"""
Módulo para interactuar con SharePoint usando Microsoft Graph API.
Adaptado para la aplicación de análisis AENC y TFROC.
"""

import streamlit as st
import requests
import os
from config.constants import SHAREPOINT_CONFIG


class SharePointClient:
    """
    Clase para manejar operaciones con SharePoint usando Microsoft Graph API.
    """
    
    def __init__(self, token):
        """
        Inicializa el cliente de SharePoint.
        
        Args:
            token (str): Token de acceso de Azure AD.
        """
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        self.site_url = SHAREPOINT_CONFIG['url']
        self.site_name = SHAREPOINT_CONFIG['site']
    
    def get_site_id(self):
        """
        Obtiene el ID del sitio de SharePoint.
        
        Returns:
            str or None: ID del sitio si se encuentra, None en caso contrario.
        """
        try:
            # Obtener información del sitio usando el formato correcto para Microsoft Graph API
            # Formato: https://graph.microsoft.com/v1.0/sites/{hostname}:/sites/{site-name}
            hostname = self.site_url.replace("https://", "").replace("http://", "")
            url = f"https://graph.microsoft.com/v1.0/sites/{hostname}:/sites/{self.site_name}"
            
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                site_data = response.json()
                site_id = site_data.get('id')
                if site_id:
                    return site_id
                else:
                    st.error("❌ No se pudo obtener el ID del sitio")
                    return None
            else:
                st.error(f"❌ Error al obtener ID del sitio: {response.status_code}")
                
                # Proporcionar información de diagnóstico
                if response.status_code == 401:
                    st.error("🔐 Error de autenticación. Verifica que el token sea válido.")
                elif response.status_code == 403:
                    st.error("🚫 Error de permisos. Verifica que la aplicación tenga permisos para acceder al sitio.")
                elif response.status_code == 404:
                    st.error("🔍 Sitio no encontrado. Verifica que el nombre del sitio sea correcto.")
                
                return None
                
        except Exception as e:
            st.error(f"❌ Error al obtener ID del sitio: {str(e)}")
            return None
    
    def get_folder(self, folder_path):
        """
        Obtiene una carpeta de SharePoint.
        
        Args:
            folder_path (str): Ruta de la carpeta en SharePoint
            
        Returns:
            dict or None: Información de la carpeta si existe, None en caso contrario.
        """
        try:
            site_id = self.get_site_id()
            if not site_id:
                return None
            
            # Obtener información de la carpeta
            url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{folder_path}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error al obtener carpeta {folder_path}: {response.status_code}")
                return None
                
        except Exception as e:
            st.error(f"Error al obtener carpeta {folder_path}: {str(e)}")
            return None
    
    def list_files(self, folder_path):
        """
        Lista archivos en una carpeta de SharePoint.
        
        Args:
            folder_path (str): Ruta de la carpeta en SharePoint
            
        Returns:
            list: Lista de archivos en la carpeta.
        """
        try:
            site_id = self.get_site_id()
            if not site_id:
                return []
            
            # Obtener archivos de la carpeta
            url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{folder_path}:/children"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('value', [])
            else:
                st.error(f"Error al listar archivos en {folder_path}: {response.status_code}")
                return []
                
        except Exception as e:
            st.error(f"Error al listar archivos en {folder_path}: {str(e)}")
            return []
    
    def check_files_by_priority(self, folder_path, prefix):
        """
        Verifica archivos por prioridad (.TxF > .TxR > .Tx2) en SharePoint.
        
        Args:
            folder_path (str): Ruta de la carpeta en SharePoint
            prefix (str): Prefijo del archivo (aenc o tfroc)
            
        Returns:
            dict: Diccionario con archivos por prioridad
        """
        files = self.list_files(folder_path)
        
        # Filtrar archivos por prefijo y extensión
        txf_files = [
            file['name'] for file in files 
            if file['name'].startswith(prefix) and file['name'].endswith(".TxF")
        ]
        txr_files = [
            file['name'] for file in files 
            if file['name'].startswith(prefix) and file['name'].endswith(".TxR")
        ]
        tx2_files = [
            file['name'] for file in files 
            if file['name'].startswith(prefix) and file['name'].endswith(".Tx2")
        ]
        
        return {
            'txf': txf_files,
            'txr': txr_files,
            'tx2': tx2_files
        }
    
    def verify_files_before_download(self, year, month):
        """
        Verifica si ya existen archivos en SharePoint antes de descargar del FTP
        Sigue la jerarquía: .TxF > .TxR > .Tx2
        Retorna True si existen archivos de alta prioridad, False si necesita descargar
        """
        try:
            # Convertir month a entero si es string
            if isinstance(month, str):
                month_int = int(month)
            else:
                month_int = month
            
            folder_path = f"aenc_pruebas/{year}/{month_int:02d}"
            
            st.info(f"🔍 Verificando carpeta: {folder_path}")
            
            # Verificar archivos AENC por prioridad
            aenc_files = self.check_files_by_priority(folder_path, "aenc")
            tfroc_files = self.check_files_by_priority(folder_path, "tfroc")
            
            # Mostrar información consolidada de archivos encontrados
            st.info(f"📋 Archivos encontrados en SharePoint:")
            if aenc_files['txf']:
                st.info(f"   • AENC .TxF: {len(aenc_files['txf'])} archivos")
            if aenc_files['txr']:
                st.info(f"   • AENC .TxR: {len(aenc_files['txr'])} archivos")
            if aenc_files['tx2']:
                st.info(f"   • AENC .Tx2: {len(aenc_files['tx2'])} archivos")
            if tfroc_files['txf']:
                st.info(f"   • TFROC .TxF: {len(tfroc_files['txf'])} archivos")
            if tfroc_files['txr']:
                st.info(f"   • TFROC .TxR: {len(tfroc_files['txr'])} archivos")
            if tfroc_files['tx2']:
                st.info(f"   • TFROC .Tx2: {len(tfroc_files['tx2'])} archivos")
            
            # Determinar si necesita descargar basándose en la jerarquía
            needs_download = False
            
            # Si hay archivos .TxF, no necesita descargar
            if aenc_files['txf'] or tfroc_files['txf']:
                st.success(f"✅ Archivos .TxF encontrados en SharePoint para {year}-{month_int:02d}")
                st.info("🔄 NO necesita descargar del FTP")
                return True
            
            # Si no hay .TxF pero hay .TxR, verificar si son suficientes
            elif aenc_files['txr'] or tfroc_files['txr']:
                st.warning(f"⚠️ Solo archivos .TxR encontrados en SharePoint para {year}-{month_int:02d}")
                st.info("🔄 Descargando archivos del FTP para obtener versiones .TxF...")
                needs_download = True
            
            # Si solo hay .Tx2 o no hay archivos, necesita descargar
            elif aenc_files['tx2'] or tfroc_files['tx2']:
                st.warning(f"⚠️ Solo archivos .Tx2 encontrados en SharePoint para {year}-{month_int:02d}")
                st.info("🔄 Descargando archivos del FTP para obtener versiones .TxF...")
                needs_download = True
            
            else:
                st.info(f"📁 No se encontraron archivos en SharePoint para {year}-{month_int:02d}")
                st.info("✅ Procediendo con la descarga del FTP...")
                needs_download = True
            
            st.info(f"🔍 RESULTADO: {'NO descargar' if not needs_download else 'SÍ descargar'}")
            return not needs_download
                
        except Exception as e:
            st.error(f"Error al verificar archivos en SharePoint: {e}")
            return False
    
    def upload_file(self, folder_path, file_path, file_name):
        """
        Sube un archivo a SharePoint.
        
        Args:
            folder_path (str): Ruta de la carpeta en SharePoint
            file_path (str): Ruta local del archivo
            file_name (str): Nombre del archivo en SharePoint
            
        Returns:
            bool: True si la subida es exitosa, False en caso contrario
        """
        try:
            site_id = self.get_site_id()
            if not site_id:
                return False
            
            # Leer archivo local
            with open(file_path, "rb") as file:
                file_content = file.read()
            
            # Subir archivo
            url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{folder_path}/{file_name}:/content"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/octet-stream"
            }
            
            response = requests.put(url, data=file_content, headers=headers)
            
            if response.status_code in [200, 201]:
                return True
            else:
                st.error(f"❌ Error al subir {file_name}: {response.status_code}")
                return False
                
        except Exception as e:
            st.error(f"❌ Error al subir {file_name}: {str(e)}")
            return False
    
    def upload_files_from_folder(self, folder_path, local_folder, file_names):
        """
        Sube múltiples archivos desde una carpeta local.
        
        Args:
            folder_path (str): Ruta de la carpeta en SharePoint
            local_folder (str): Carpeta local con los archivos
            file_names (list): Lista de nombres de archivos a subir
            
        Returns:
            int: Número de archivos subidos exitosamente
        """
        uploaded_count = 0
        progress_bar = st.progress(0)
        
        for i, file_name in enumerate(file_names):
            local_path = os.path.join(local_folder, file_name)
            
            if os.path.exists(local_path):
                if self.upload_file(folder_path, local_path, file_name):
                    uploaded_count += 1
            
            # Actualizar barra de progreso
            progress = (i + 1) / len(file_names)
            progress_bar.progress(progress)
        
        progress_bar.empty()
        return uploaded_count
    
    def upload_files_batch(self, folder_path, local_folder, file_names, batch_size=10):
        """
        Sube archivos en lotes para mejorar la eficiencia.
        
        Args:
            folder_path (str): Ruta de la carpeta en SharePoint
            local_folder (str): Carpeta local con los archivos
            file_names (list): Lista de nombres de archivos a subir
            batch_size (int): Tamaño del lote para procesar
            
        Returns:
            int: Número de archivos subidos exitosamente
        """
        uploaded_count = 0
        failed_files = []
        total_batches = (len(file_names) + batch_size - 1) // batch_size
        
        # Mostrar información consolidada
        st.info(f"📤 Subiendo {len(file_names)} archivos en {total_batches} lotes...")
        
        progress_bar = st.progress(0)
        
        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(file_names))
            batch_files = file_names[start_idx:end_idx]
            
            # Procesar lote actual
            for i, file_name in enumerate(batch_files):
                local_path = os.path.join(local_folder, file_name)
                
                if os.path.exists(local_path):
                    if self.upload_file(folder_path, local_path, file_name):
                        uploaded_count += 1
                    else:
                        failed_files.append(file_name)
                else:
                    failed_files.append(file_name)
                
                # Actualizar barra de progreso
                overall_progress = (start_idx + i + 1) / len(file_names)
                progress_bar.progress(overall_progress)
            
            # Mostrar progreso del lote
            if batch_num < total_batches - 1:
                st.info(f"📦 Lote {batch_num + 1}/{total_batches} completado")
        
        progress_bar.empty()
        
        # Mostrar resumen consolidado
        if failed_files:
            st.warning(f"⚠️ {len(failed_files)} archivos fallaron en la subida")
        else:
            st.success(f"✅ Todos los archivos subidos exitosamente")
        
        return uploaded_count
    
    def clean_files_by_priority(self, folder_path, uploaded_files):
        """
        Limpia archivos en SharePoint según la jerarquía TxF > TxR > Tx2.
        
        Args:
            folder_path (str): Ruta de la carpeta en SharePoint
            uploaded_files (list): Lista de archivos subidos
        """
        try:
            files = self.list_files(folder_path)
            file_names = [file['name'] for file in files]
            
            # Separar archivos por extensión
            txf_files = [f for f in file_names if f.endswith(".TxF")]
            txr_files = [f for f in file_names if f.endswith(".TxR")]
            tx2_files = [f for f in file_names if f.endswith(".Tx2")]
            
            files_to_delete = []
            
            # Si existen archivos TxF, borrar TxR y Tx2
            if txf_files:
                files_to_delete.extend(txr_files + tx2_files)
            # Si no hay TxF pero hay TxR, borrar solo Tx2
            elif txr_files:
                files_to_delete.extend(tx2_files)
            
            # Borrar archivos seleccionados
            for file_name in files_to_delete:
                try:
                    self.delete_file(folder_path, file_name)
                    st.info(f"🗑️ Archivo eliminado: {file_name}")
                except Exception as e:
                    st.warning(f"⚠️ No se pudo eliminar {file_name}: {str(e)}")
                    
        except Exception as e:
            st.error(f"❌ Error al limpiar archivos: {str(e)}")
    
    def delete_file(self, folder_path, file_name):
        """
        Elimina un archivo de SharePoint.
        
        Args:
            folder_path (str): Ruta de la carpeta en SharePoint
            file_name (str): Nombre del archivo a eliminar
            
        Returns:
            bool: True si la eliminación es exitosa, False en caso contrario
        """
        try:
            site_id = self.get_site_id()
            if not site_id:
                return False
            
            url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{folder_path}/{file_name}"
            response = requests.delete(url, headers=self.headers)
            
            return response.status_code == 204
            
        except Exception as e:
            st.error(f"Error al eliminar archivo {file_name}: {str(e)}")
            return False
    
    def get_folder_path(self, year, month):
        """
        Genera la ruta de la carpeta en SharePoint.
        
        Args:
            year (int): Año
            month (str): Mes en formato MM
            
        Returns:
            str: Ruta de la carpeta en SharePoint
        """
        return f"aenc_pruebas/{year}/{month}"
    
    def process_month_upload(self, year, month, local_folder="archivos_descargados"):
        """
        Procesa la subida de archivos para un mes específico.
        
        Args:
            year (int): Año
            month (str): Mes en formato MM
            local_folder (str): Carpeta local con los archivos
            
        Returns:
            bool: True si el proceso es exitoso, False en caso contrario
        """
        folder_path = self.get_folder_path(year, month)
        
        # Verificar si ya existen archivos de alta prioridad (.TxF)
        aenc_files = self.check_files_by_priority(folder_path, "aenc")
        tfroc_files = self.check_files_by_priority(folder_path, "tfroc")
        
        if aenc_files['txf'] or tfroc_files['txf']:
            st.warning(f"⚠️ Archivos .TxF ya existen en SharePoint para {year}-{month}. No se subirán archivos.")
            if aenc_files['txf']:
                st.info(f"AENC .TxF existentes: {', '.join(aenc_files['txf'])}")
            if tfroc_files['txf']:
                st.info(f"TFROC .TxF existentes: {', '.join(tfroc_files['txf'])}")
            return True
        
        # Listar archivos locales
        if not os.path.exists(local_folder):
            st.error(f"❌ La carpeta {local_folder} no existe")
            return False
        
        local_files = os.listdir(local_folder)
        
        # Filtrar archivos por mes basándose en el nombre del archivo
        # Los archivos tienen formato: aencMMDD.TxF o tfrocMMDD.TxF
        # Convertir month a entero si es string y luego formatear
        if isinstance(month, str):
            month_int = int(month)
        else:
            month_int = month
        month_str = f"{month_int:02d}"  # Asegurar formato MM
        
        aenc_files = [f for f in local_files if f.startswith(f"aenc{month_str}")]
        tfroc_files = [f for f in local_files if f.startswith(f"tfroc{month_str}")]
        
        files_to_upload = aenc_files + tfroc_files
        
        if not files_to_upload:
            st.info(f"ℹ️ No hay archivos para subir del mes {month} en {local_folder}")
            st.info("   Esto es normal cuando los archivos aún no están disponibles en el FTP")
            return True  # No es un error, es un caso normal
        
        st.info(f"📤 Subiendo {len(files_to_upload)} archivos a SharePoint...")
        
        # Usar carga en lotes para mejor eficiencia
        uploaded_count = self.upload_files_batch(folder_path, local_folder, files_to_upload, batch_size=15)
        
        if uploaded_count > 0:
            # Limpiar archivos según prioridad
            self.clean_files_by_priority(folder_path, files_to_upload)
            st.success(f"✅ Proceso completado: {uploaded_count} archivos subidos")
            return True
        else:
            st.error("❌ No se pudo subir ningún archivo")
            return False
    
    def upload_processed_files(self, year, month, file_content, file_name):
        """
        Sube archivos procesados (CSV) a SharePoint.
        
        Args:
            year (int): Año
            month (str): Mes en formato MM
            file_content (bytes): Contenido del archivo
            file_name (str): Nombre del archivo
            
        Returns:
            bool: True si la subida es exitosa, False en caso contrario
        """
        try:
            folder_path = self.get_folder_path(year, month)
            site_id = self.get_site_id()
            if not site_id:
                return False
            
            url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{folder_path}/{file_name}:/content"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/octet-stream"
            }
            
            response = requests.put(url, data=file_content, headers=headers)
            
            if response.status_code in [200, 201]:
                st.success(f"✅ Archivo procesado subido: {file_name}")
                return True
            else:
                st.error(f"❌ Error al subir archivo procesado {file_name}: {response.status_code}")
                return False
                
        except Exception as e:
            st.error(f"❌ Error al subir archivo procesado {file_name}: {str(e)}")
            return False
    
    def update_annual_consumption_file(self, year, month, new_data_content):
        """
        Actualiza el archivo de consumo anual en la carpeta fact_consumos.
        
        Args:
            year (int): Año
            month (str): Mes en formato MM
            new_data_content (bytes): Contenido del archivo actualizado
            
        Returns:
            bool: True si la actualización es exitosa, False en caso contrario
        """
        try:
            folder_path = "aenc_pruebas/fact_consumos"
            file_name = f"consumos_{year}.csv"
            site_id = self.get_site_id()
            if not site_id:
                return False
            
            url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{folder_path}/{file_name}:/content"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/octet-stream"
            }
            
            response = requests.put(url, data=new_data_content, headers=headers)
            
            if response.status_code in [200, 201]:
                st.success(f"✅ Archivo anual actualizado: {file_name}")
                return True
            else:
                st.error(f"❌ Error al actualizar archivo anual {file_name}: {response.status_code}")
                return False
                
        except Exception as e:
            st.error(f"❌ Error al actualizar archivo anual {file_name}: {str(e)}")
            return False
    
    def download_file_content(self, folder_path, file_name):
        """
        Descarga el contenido de un archivo desde SharePoint.
        
        Args:
            folder_path (str): Ruta de la carpeta en SharePoint
            file_name (str): Nombre del archivo
            
        Returns:
            bytes or None: Contenido del archivo si la descarga es exitosa, None en caso contrario
        """
        try:
            site_id = self.get_site_id()
            if not site_id:
                return None
            
            url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{folder_path}/{file_name}:/content"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                return response.content
            else:
                st.error(f"Error al descargar archivo {file_name}: {response.status_code}")
                return None
                
        except Exception as e:
            st.error(f"Error al descargar archivo {file_name}: {str(e)}")
            return None
    
    def test_connection(self):
        """
        Prueba la conexión con SharePoint.
        
        Returns:
            bool: True si la conexión es exitosa, False en caso contrario.
        """
        try:
            hostname = self.site_url.replace("https://", "").replace("http://", "")
            url = f"https://graph.microsoft.com/v1.0/sites/{hostname}:/sites/{self.site_name}"
            
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                site_data = response.json()
                site_id = site_data.get('id')
                if site_id:
                    return True
                else:
                    return False
            else:
                return False
                
        except Exception as e:
            return False
