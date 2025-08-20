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
            month (str): Mes en formato MM
            
        Returns:
            str: Ruta del archivo en el servidor FTP
        """
        return f"/INFORMACION_XM/USUARIOSK/RTQC/sic/comercia/{year}-{month}"
    
    def list_files(self, year, month):
        """
        Lista los archivos disponibles en el servidor FTP para un año y mes específicos.
        
        Args:
            year (int): Año
            month (str): Mes en formato MM
            
        Returns:
            list: Lista de archivos disponibles
        """
        if not self.connection:
            st.error("❌ No hay conexión FTP activa")
            return []
        
        try:
            file_path = self.get_file_path(year, month)
            st.info(f"📁 Navegando a: {file_path}")
            
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
        
        Args:
            files (list): Lista de archivos
            prefix (str): Prefijo del archivo (aenc o tfroc)
            
        Returns:
            list: Lista de archivos filtrados por prioridad
        """
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
            with open(local_path, "wb") as f:
                self.connection.retrbinary(f"RETR {filename}", f.write)
            
            st.success(f"✅ Archivo descargado: {filename}")
            return True
            
        except Exception as e:
            st.error(f"❌ Error al descargar {filename}: {str(e)}")
            return False
    
    def download_month_files(self, year, month, temp_folder="archivos_descargados"):
        """
        Descarga los archivos AENC y TFROC para un mes específico.
        
        Args:
            year (int): Año
            month (str): Mes en formato MM
            temp_folder (str): Carpeta temporal para almacenar archivos
            
        Returns:
            list: Lista de archivos descargados exitosamente
        """
        # Crear carpeta temporal si no existe
        os.makedirs(temp_folder, exist_ok=True)
        
        # Listar archivos disponibles
        files = self.list_files(year, month)
        if not files:
            return []
        
        # Filtrar archivos por prioridad
        aenc_files = self.filter_files_by_priority(files, "aenc")
        tfroc_files = self.filter_files_by_priority(files, "tfroc")
        
        # Combinar archivos a descargar
        files_to_download = aenc_files + tfroc_files
        
        if not files_to_download:
            st.warning("⚠️ No se encontraron archivos AENC o TFROC para descargar")
            return []
        
        st.info(f"📥 Descargando {len(files_to_download)} archivos...")
        
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
