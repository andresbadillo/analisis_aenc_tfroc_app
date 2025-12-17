"""
Módulo para manejar la conexión FTP y descarga de archivos AENC y TFROC.
"""

import streamlit as st
from ftplib import FTP_TLS
import os
from datetime import datetime, timedelta
from config.constants import FTP_CONFIG, FILE_VERSION_PRIORITY


class FTPClient:
    """
    Clase para manejar operaciones con el servidor FTP de XM.
    """
    
    def __init__(self):
        """Inicializa el cliente FTP."""
        self.connection = None
        self.server = FTP_CONFIG['server']
        self.port = FTP_CONFIG['port']
        self.user = FTP_CONFIG['user']
        self.password = FTP_CONFIG['password']
    
    def connect(self):
        """
        Establece conexión con el servidor FTP.
        
        Returns:
            bool: True si la conexión es exitosa, False en caso contrario.
        """
        try:
            st.info("🔌 Conectando al servidor FTP...")
            
            self.connection = FTP_TLS()
            self.connection.connect(self.server, self.port)
            self.connection.login(user=self.user, passwd=self.password)
            self.connection.set_pasv(True)
            self.connection.prot_p()
            
            st.success("✅ Conexión FTP establecida exitosamente")
            return True
            
        except Exception as e:
            st.error(f"❌ Error al conectar al FTP: {str(e)}")
            return False
    
    def disconnect(self):
        """Cierra la conexión FTP."""
        if self.connection:
            try:
                self.connection.quit()
                st.info("🔌 Conexión FTP cerrada")
            except:
                pass
            finally:
                self.connection = None
    
    def get_file_path(self, year, month):
        """
        Genera la ruta del archivo en el servidor FTP.
        
        Args:
            year (int): Año
            month (int or str): Mes (se convertirá a formato MM)
            
        Returns:
            str: Ruta del archivo en el servidor FTP
        """
        # Asegurar que el mes tenga dos dígitos
        if isinstance(month, str):
            month_int = int(month)
        else:
            month_int = month
        
        month_formatted = f"{month_int:02d}"
        return f"/INFORMACION_XM/USUARIOSK/RTQC/sic/comercia/{year}-{month_formatted}"
    
    def list_files(self, year, month):
        """
        Lista los archivos disponibles en el servidor FTP para un año y mes específicos.
        
        Args:
            year (int): Año
            month (int or str): Mes (se convertirá a formato MM)
            
        Returns:
            list: Lista de archivos disponibles
        """
        if not self.connection:
            st.error("❌ No hay conexión FTP activa")
            return []
        
        try:
            file_path = self.get_file_path(year, month)
            self.connection.cwd(file_path)
            files = self.connection.nlst()
            st.success(f"✅ Encontrados {len(files)} archivos")
            return files
            
        except Exception as e:
            st.error(f"❌ Error al listar archivos: {str(e)}")
            return []
    
    def filter_files_by_priority(self, files, prefix):
        """
        Filtra archivos por prefijo y prioridad de versión.
        SOLO archivos aenc y tfroc
        
        Args:
            files (list): Lista de archivos
            prefix (str): Prefijo del archivo (aenc o tfroc)
            
        Returns:
            list: Lista de archivos filtrados por prioridad
        """
        # Validar que el prefijo sea solo aenc o tfroc
        if prefix not in ['aenc', 'tfroc']:
            st.warning(f"⚠️ Prefijo '{prefix}' no es válido. Solo se permiten 'aenc' y 'tfroc'")
            return []
        
        for extension in FILE_VERSION_PRIORITY:
            filtered_files = [
                file for file in files 
                if file.startswith(prefix) and file.endswith(extension)
            ]
            if filtered_files:
                return filtered_files
        return []
    
    def download_file(self, filename, local_path):
        """
        Descarga un archivo del servidor FTP.
        
        Args:
            filename (str): Nombre del archivo a descargar
            local_path (str): Ruta local donde guardar el archivo
            
        Returns:
            bool: True si la descarga es exitosa, False en caso contrario
        """
        if not self.connection:
            st.error("❌ No hay conexión FTP activa")
            return False
        
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Usar callback explícito para asegurar escritura correcta en aplicaciones empaquetadas
            def write_callback(data):
                """Callback para escribir datos en el archivo."""
                file_handle.write(data)
            
            with open(local_path, "wb") as file_handle:
                # Descargar archivo usando callback explícito
                self.connection.retrbinary(f"RETR {filename}", write_callback)
                # Asegurar que el buffer se vacíe antes de cerrar
                file_handle.flush()
                # Forzar sincronización del sistema de archivos
                os.fsync(file_handle.fileno())
            
            # Verificar que el archivo se descargó correctamente (no esté vacío)
            if os.path.exists(local_path):
                file_size = os.path.getsize(local_path)
                if file_size == 0:
                    st.error(f"❌ El archivo {filename} se descargó pero está vacío (0 bytes)")
                    try:
                        os.remove(local_path)  # Eliminar archivo vacío
                    except:
                        pass
                    return False
                return True
            else:
                st.error(f"❌ El archivo {filename} no se creó correctamente")
                return False
            
        except Exception as e:
            st.error(f"❌ Error al descargar {filename}: {str(e)}")
            # Limpiar archivo parcial si existe
            if os.path.exists(local_path):
                try:
                    os.remove(local_path)
                except:
                    pass
            return False
    
    def download_month_files(self, year, month, temp_folder=None, sharepoint_info=None):
        # Si no se especifica temp_folder, usar la ruta por defecto
        if temp_folder is None:
            # Usar ruta fija en lugar de importar desde app.py
            downloads_path = os.path.expanduser("~/Downloads")
            if not os.path.exists(downloads_path):
                # Fallback para Windows si no encuentra Downloads
                downloads_path = os.path.expanduser("~/OneDrive/Downloads")
                if not os.path.exists(downloads_path):
                    # Fallback final: carpeta del proyecto
                    downloads_path = os.getcwd()
            temp_folder = os.path.join(downloads_path, "archivos_descargados")
        """
        Descarga los archivos AENC y TFROC para un mes específico con lógica corregida.
        
        Args:
            year (int): Año
            month (int or str): Mes (se convertirá a formato MM)
            temp_folder (str): Carpeta temporal para almacenar archivos
            sharepoint_info (dict): Información de SharePoint con estrategia y archivos
            
        Returns:
            list: Lista de archivos descargados exitosamente
        """
        try:
            # Crear carpeta temporal si no existe
            os.makedirs(temp_folder, exist_ok=True)
            
            # LÓGICA CORREGIDA: Implementar la estrategia según SharePoint
            if sharepoint_info and sharepoint_info.get('strategy') == 'none':
                st.info("✅ No se necesita descargar - Ya existen archivos .TxF en SharePoint")
                return []
            
            # Listar archivos disponibles en FTP
            files = self.list_files(year, month)
            
            if not files:
                st.warning(f"⚠️ No se encontraron archivos en el FTP para {year}-{month}")
                return []
            
            # Determinar qué archivos descargar según la estrategia
            files_to_download = []
            
            if sharepoint_info and sharepoint_info.get('strategy') == 'check_ftp':
                # Verificar si hay archivos .TxF de aenc y tfroc en el FTP
                aenc_txf_files = [f for f in files if f.startswith("aenc") and f.endswith(".TxF")]
                tfroc_txf_files = [f for f in files if f.startswith("tfroc") and f.endswith(".TxF")]
                txf_files = aenc_txf_files + tfroc_txf_files
                
                if txf_files:
                    st.info(f"🎯 Encontrados {len(txf_files)} archivos .TxF (aenc: {len(aenc_txf_files)}, tfroc: {len(tfroc_txf_files)}) en FTP - Descargando para reemplazar .TxR")
                    files_to_download = txf_files
                else:
                    st.info("ℹ️ No hay archivos .TxF de aenc/tfroc en FTP - No se descargan archivos (mantener .TxR existentes)")
                    return []
            
            elif sharepoint_info and sharepoint_info.get('strategy') == 'download':
                # Descargar con prioridad .TxF > .TxR > .Tx2
                st.info("🔄 Descargando archivos del FTP con prioridad .TxF > .TxR > .Tx2")
                files_to_download = self._get_files_to_download_by_priority(files)
            
            else:
                # Estrategia por defecto: descargar con prioridad
                st.info("🔄 Descargando archivos del FTP con prioridad estándar")
                files_to_download = self._get_files_to_download_by_priority(files)
            
            if not files_to_download:
                st.warning(f"⚠️ No se encontraron archivos AENC o TFROC para descargar en {year}-{month}")
                return []
            
            # Mostrar información consolidada
            st.info(f"📥 Descargando {len(files_to_download)} archivos del FTP ({year}-{month})")
            
            # Separar archivos por tipo para mostrar información
            aenc_files = [f for f in files_to_download if f.startswith("aenc")]
            tfroc_files = [f for f in files_to_download if f.startswith("tfroc")]
            
            if aenc_files:
                st.info(f"   • AENC: {len(aenc_files)} archivos")
            if tfroc_files:
                st.info(f"   • TFROC: {len(tfroc_files)} archivos")
            
            downloaded_files = []
            progress_bar = st.progress(0)
            
            for i, filename in enumerate(files_to_download):
                local_path = os.path.join(temp_folder, filename)
                
                if self.download_file(filename, local_path):
                    downloaded_files.append(filename)
                
                # Actualizar barra de progreso
                progress = (i + 1) / len(files_to_download)
                progress_bar.progress(progress)
            
            progress_bar.empty()
            
            if downloaded_files:
                st.success(f"✅ Descarga completada: {len(downloaded_files)} archivos")
            else:
                st.error("❌ No se pudo descargar ningún archivo")
            
            return downloaded_files
            
        except Exception as e:
            st.error(f"❌ Error en download_month_files para {year}-{month}: {str(e)}")
            return []
    
    def _get_files_to_download_by_priority(self, files):
        """
        Obtiene archivos para descargar siguiendo la prioridad .TxF > .TxR > .Tx2
        SOLO archivos aenc y tfroc
        
        Args:
            files (list): Lista de archivos disponibles en FTP
            
        Returns:
            list: Lista de archivos a descargar (solo aenc y tfroc)
        """
        files_to_download = []
        
        # Filtrar solo archivos aenc y tfroc
        aenc_tf_files = [f for f in files if f.startswith("aenc") and f.endswith(".TxF")]
        tfroc_tf_files = [f for f in files if f.startswith("tfroc") and f.endswith(".TxF")]
        txf_files = aenc_tf_files + tfroc_tf_files
        
        if txf_files:
            st.info(f"🎯 Encontrados {len(txf_files)} archivos .TxF (aenc: {len(aenc_tf_files)}, tfroc: {len(tfroc_tf_files)}) - Prioridad máxima")
            files_to_download.extend(txf_files)
            return files_to_download
        
        # Si no hay .TxF, buscar archivos .TxR (solo aenc y tfroc)
        aenc_tr_files = [f for f in files if f.startswith("aenc") and f.endswith(".TxR")]
        tfroc_tr_files = [f for f in files if f.startswith("tfroc") and f.endswith(".TxR")]
        txr_files = aenc_tr_files + tfroc_tr_files
        
        if txr_files:
            st.info(f"🎯 Encontrados {len(txr_files)} archivos .TxR (aenc: {len(aenc_tr_files)}, tfroc: {len(tfroc_tr_files)}) - Segunda prioridad")
            files_to_download.extend(txr_files)
            return files_to_download
        
        # Si no hay .TxF ni .TxR, buscar archivos .Tx2 (solo aenc y tfroc)
        aenc_t2_files = [f for f in files if f.startswith("aenc") and f.endswith(".Tx2")]
        tfroc_t2_files = [f for f in files if f.startswith("tfroc") and f.endswith(".Tx2")]
        tx2_files = aenc_t2_files + tfroc_t2_files
        
        if tx2_files:
            st.info(f"🎯 Encontrados {len(tx2_files)} archivos .Tx2 (aenc: {len(aenc_t2_files)}, tfroc: {len(tfroc_t2_files)}) - Última prioridad")
            files_to_download.extend(tx2_files)
            return files_to_download
        
        return files_to_download
    
    def get_previous_month(self, year, month):
        """
        Obtiene el año y mes anterior.
        
        Args:
            year (int): Año actual
            month (str): Mes actual en formato MM
            
        Returns:
            tuple: (año_anterior, mes_anterior)
        """
        current_date = datetime(year, int(month), 1)
        previous_month = current_date - timedelta(days=1)
        return previous_month.year, f"{previous_month.month:02d}"
    
    def process_current_and_previous_month(self):
        """
        Procesa el mes actual y el mes anterior.
        
        Returns:
            dict: Diccionario con los archivos descargados por mes
        """
        current_year = datetime.now().year
        current_month = f"{datetime.now().month:02d}"
        
        previous_year, previous_month = self.get_previous_month(current_year, int(current_month))
        
        results = {}
        
        # Procesar mes anterior
        st.subheader(f"📅 Procesando mes anterior: {previous_month}/{previous_year}")
        results[f"{previous_year}-{previous_month}"] = self.download_month_files(
            previous_year, previous_month
        )
        
        # Procesar mes actual
        st.subheader(f"📅 Procesando mes actual: {current_month}/{current_year}")
        results[f"{current_year}-{current_month}"] = self.download_month_files(
            current_year, current_month
        )
        
        return results
