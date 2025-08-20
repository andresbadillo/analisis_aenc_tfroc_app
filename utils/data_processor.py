"""
Módulo para procesar los datos AENC y TFROC.
"""

import streamlit as st
import pandas as pd
import holidays_co
import io
from datetime import datetime
from pathlib import Path
from config.constants import OR_MAPPING, DIAS_SEMANA, TIPOS_DIA


class DataProcessor:
    """
    Clase para procesar los datos AENC y TFROC.
    """
    
    def __init__(self):
        """Inicializa el procesador de datos."""
        pass
    
    def get_day_of_week(self, date_str):
        """
        Obtiene el nombre del día de la semana en español.
        
        Args:
            date_str (str): Fecha en formato dd-mm-yyyy
            
        Returns:
            str: Nombre del día de la semana
        """
        try:
            date_obj = datetime.strptime(date_str, "%d-%m-%Y")
            day_index = date_obj.weekday()
            return DIAS_SEMANA[day_index]
        except Exception as e:
            st.error(f"❌ Error al obtener día de la semana: {str(e)}")
            return "Desconocido"
    
    def get_day_type(self, date_str):
        """
        Determina el tipo de día (Hábil, Sábado, Domingo, Festivo).
        
        Args:
            date_str (str): Fecha en formato dd-mm-yyyy
            
        Returns:
            str: Tipo de día
        """
        try:
            date_obj = datetime.strptime(date_str, "%d-%m-%Y").date()
            
            # Verificar si es festivo
            if holidays_co.is_holiday_date(date_obj):
                return "Festivo"
            
            # Obtener tipo de día según el día de la semana
            day_index = date_obj.weekday()
            return TIPOS_DIA[day_index]
            
        except Exception as e:
            st.error(f"❌ Error al determinar tipo de día: {str(e)}")
            return "Desconocido"
    
    def map_nt_by_range(self, value):
        """
        Mapea el nivel de tensión por rangos.
        
        Args:
            value (float): Valor del nivel de tensión
            
        Returns:
            int: Nivel de tensión mapeado
        """
        try:
            value = float(value)
            if value in {1, 2}:
                return int(value)
            elif value < 1:
                return 1
            elif value < 30:
                return 2
            elif value < 57.5:
                return 3
            else:
                return None
        except:
            return None
    
    def load_files_from_sharepoint(self, folder, valid_extensions):
        """
        Carga archivos AENC y TFROC desde SharePoint.
        
        Args:
            folder: Objeto de carpeta de SharePoint
            valid_extensions (tuple): Extensiones válidas de archivos
            
        Returns:
            tuple: (archivos_aenc, archivos_tfroc)
        """
        try:
            files = folder.files
            aenc_files = [
                file for file in files 
                if 'aenc' in file['Name'] and file['Name'].endswith(valid_extensions)
            ]
            tfroc_files = [
                file for file in files 
                if 'tfroc' in file['Name'] and file['Name'].endswith(valid_extensions)
            ]
            return aenc_files, tfroc_files
        except Exception as e:
            st.error(f"❌ Error al cargar archivos desde SharePoint: {str(e)}")
            return [], []
    
    def load_files_from_sharepoint_new(self, files, valid_extensions):
        """
        Carga archivos AENC y TFROC desde SharePoint usando la nueva API.
        
        Args:
            files: Lista de archivos de SharePoint
            valid_extensions (tuple): Extensiones válidas de archivos
            
        Returns:
            tuple: (archivos_aenc, archivos_tfroc)
        """
        try:
            aenc_files = [
                file for file in files 
                if 'aenc' in file['name'] and file['name'].endswith(valid_extensions)
            ]
            tfroc_files = [
                file for file in files 
                if 'tfroc' in file['name'] and file['name'].endswith(valid_extensions)
            ]
            return aenc_files, tfroc_files
        except Exception as e:
            st.error(f"❌ Error al cargar archivos desde SharePoint: {str(e)}")
            return [], []
    
    def process_aenc_file(self, aenc_content, date):
        """
        Procesa un archivo AENC.
        
        Args:
            aenc_content (bytes): Contenido del archivo AENC
            date (str): Fecha en formato dd-mm-yyyy
            
        Returns:
            pd.DataFrame: DataFrame procesado
        """
        try:
            # Leer el archivo CSV
            df = pd.read_csv(io.BytesIO(aenc_content), sep=";", encoding='latin1')
            
            # Renombrar columnas
            df.rename(columns={"CODIGO SIC": "CODIGO FRONTERA"}, inplace=True)
            
            # Obtener columnas de horas
            horas = [col for col in df.columns if "HORA" in col]
            
            # Agregar columnas adicionales
            df.insert(0, "FECHA", date)
            df.insert(1, "DIA", self.get_day_of_week(date))
            df.insert(2, "TIPO_DIA", self.get_day_type(date))
            df["TOTAL CONSUMO"] = df.loc[:, horas].sum(axis=1)
            
            return df
            
        except Exception as e:
            st.error(f"❌ Error al procesar archivo AENC: {str(e)}")
            return None
    
    def process_tfroc_file(self, tfroc_content):
        """
        Procesa un archivo TFROC.
        
        Args:
            tfroc_content (bytes): Contenido del archivo TFROC
            
        Returns:
            pd.DataFrame: DataFrame procesado
        """
        try:
            # Leer el archivo CSV
            df = pd.read_csv(io.BytesIO(tfroc_content), sep=";", encoding='latin1')
            return df
        except Exception as e:
            st.error(f"❌ Error al procesar archivo TFROC: {str(e)}")
            return None
    
    def merge_and_process_data(self, aenc_df, tfroc_df, date):
        """
        Une y procesa los datos AENC y TFROC.
        
        Args:
            aenc_df (pd.DataFrame): DataFrame AENC
            tfroc_df (pd.DataFrame): DataFrame TFROC
            date (str): Fecha en formato dd-mm-yyyy
            
        Returns:
            pd.DataFrame: DataFrame procesado y unido
        """
        try:
            # Unir los dataframes
            merged_df = pd.merge(
                aenc_df, 
                tfroc_df[["CODIGO FRONTERA", "FACTOR DE PERDIDAS", "MERCADO COMERCIALIZACIÓN QUE EXPORTA", "NIVEL DE TENSION"]], 
                on="CODIGO FRONTERA", 
                how="inner"
            )
            
            # Obtener columnas de horas
            horas = [col for col in merged_df.columns if "HORA" in col]
            
            # Dividir valores de consumo por el factor de pérdidas
            for hora in horas:
                merged_df[hora] = merged_df[hora] / merged_df["FACTOR DE PERDIDAS"]
            
            # Renombrar columnas
            merged_df.rename(columns={"CODIGO PROPIO": "NOMBRE FRONTERA"}, inplace=True)
            
            # Seleccionar columnas para el archivo de salida
            daily_df = merged_df.loc[:, [
                "CODIGO FRONTERA", "NOMBRE FRONTERA", "MERCADO COMERCIALIZACIÓN QUE EXPORTA", 
                "NIVEL DE TENSION", "TIPO DE AGRUPACIÓN", "IMPO - EXPO"
            ] + horas]
            
            # Agregar columnas adicionales
            daily_df.insert(0, "FECHA", date)
            daily_df.insert(1, "DIA", self.get_day_of_week(date))
            daily_df.insert(2, "TIPO_DIA", self.get_day_type(date))
            
            # Agregar columna OR basada en el mapeo
            daily_df.insert(6, "OR", daily_df["MERCADO COMERCIALIZACIÓN QUE EXPORTA"].map(OR_MAPPING))
            
            # Agregar columna NT basada en la función de mapeo
            daily_df.insert(8, "NT", daily_df["NIVEL DE TENSION"].map(self.map_nt_by_range))
            
            # Agregar columna de total de consumo
            daily_df["TOTAL CONSUMO"] = daily_df.loc[:, horas].sum(axis=1)
            
            return daily_df
            
        except Exception as e:
            st.error(f"❌ Error al unir y procesar datos: {str(e)}")
            return None
    
    def process_month_data(self, sharepoint_client, year, month):
        """
        Procesa todos los datos de un mes específico.
        
        Args:
            sharepoint_client: Cliente de SharePoint
            year (int): Año
            month (str): Mes en formato MM
            
        Returns:
            dict: Diccionario con los DataFrames procesados
        """
        try:
            # Obtener carpeta del mes
            folder_path = sharepoint_client.get_folder_path(year, month)
            files = sharepoint_client.list_files(folder_path)
            
            if not files:
                st.error(f"❌ No se encontraron archivos en la carpeta {folder_path}")
                return None
            
            # Cargar archivos desde SharePoint
            valid_extensions = ('.TxF', '.TxR', '.Tx2')
            aenc_files, tfroc_files = self.load_files_from_sharepoint_new(files, valid_extensions)
            
            # Verificar cantidad de archivos
            if len(aenc_files) != len(tfroc_files):
                st.error("❌ La cantidad de archivos AENC no coincide con la cantidad de archivos TFROC")
                return None
            
            st.info(f"📁 Archivos en carpeta: {len(aenc_files)} AENC y {len(tfroc_files)} TFROC")
            
            # Inicializar DataFrames consolidados
            consolidated_aenc_df = pd.DataFrame()
            consolidated_df = pd.DataFrame()
            
            # Procesar archivos día a día
            progress_bar = st.progress(0)
            
            for i, aenc_file in enumerate(aenc_files):
                # Extraer día del nombre del archivo
                day = Path(aenc_file['name']).stem[-4:]
                date = f"{day[2:]}-{day[:2]}-{year}"
                
                # Buscar archivo TFROC correspondiente
                tfroc_file = next((f for f in tfroc_files if day in f['name']), None)
                if tfroc_file is None:
                    continue
                
                # Obtener contenido de los archivos
                aenc_content = sharepoint_client.download_file_content(folder_path, aenc_file['name'])
                tfroc_content = sharepoint_client.download_file_content(folder_path, tfroc_file['name'])
                
                # Procesar archivo AENC
                aenc_df = self.process_aenc_file(aenc_content, date)
                if aenc_df is not None:
                    consolidated_aenc_df = pd.concat([consolidated_aenc_df, aenc_df], ignore_index=True)
                
                # Procesar y unir datos
                tfroc_df = self.process_tfroc_file(tfroc_content)
                if tfroc_df is not None and aenc_df is not None:
                    daily_df = self.merge_and_process_data(aenc_df, tfroc_df, date)
                    if daily_df is not None:
                        consolidated_df = pd.concat([consolidated_df, daily_df], ignore_index=True)
                
                # Actualizar barra de progreso
                progress = (i + 1) / len(aenc_files)
                progress_bar.progress(progress)
            
            progress_bar.empty()
            
            # Ordenar DataFrames
            if not consolidated_aenc_df.empty:
                consolidated_aenc_df = consolidated_aenc_df.sort_values(by=["FECHA", "CODIGO FRONTERA"])
            
            if not consolidated_df.empty:
                consolidated_df = consolidated_df.sort_values(by=["FECHA", "CODIGO FRONTERA"])
            
            return {
                'aenc_consolidated': consolidated_aenc_df,
                'consumos_consolidated': consolidated_df
            }
            
        except Exception as e:
            st.error(f"❌ Error al procesar datos del mes: {str(e)}")
            return None
    
    def generate_output_files(self, processed_data, year, month):
        """
        Genera los archivos de salida CSV.
        
        Args:
            processed_data (dict): Datos procesados
            year (int): Año
            month (str): Mes en formato MM
            
        Returns:
            dict: Diccionario con los archivos CSV generados
        """
        try:
            output_files = {}
            
            # Generar archivo AENC consolidado
            if not processed_data['aenc_consolidated'].empty:
                aenc_file_name = f"aenc_consolidado_{month}_{year}.csv"
                aenc_csv = processed_data['aenc_consolidated'].to_csv(
                    index=False, sep=",", encoding='utf-8-sig'
                )
                output_files['aenc_consolidated'] = {
                    'name': aenc_file_name,
                    'content': aenc_csv.encode('utf-8-sig')
                }
            
            # Generar archivo de consumos consolidado
            if not processed_data['consumos_consolidated'].empty:
                consumos_file_name = f"consumos_{month}_{year}.csv"
                consumos_csv = processed_data['consumos_consolidated'].to_csv(
                    index=False, sep=",", encoding='utf-8-sig'
                )
                output_files['consumos_consolidated'] = {
                    'name': consumos_file_name,
                    'content': consumos_csv.encode('utf-8-sig')
                }
                
                # Generar archivo de total de consumo por frontera
                total_consumo_df = processed_data['consumos_consolidated'].groupby(
                    ["CODIGO FRONTERA", "NOMBRE FRONTERA", "TIPO DE AGRUPACIÓN", "IMPO - EXPO"], 
                    as_index=False
                ).agg({"TOTAL CONSUMO": "sum"})
                
                total_consumo_file_name = f"total_consumo_{month}_{year}.csv"
                total_consumo_csv = total_consumo_df.to_csv(
                    index=False, sep=",", encoding='utf-8-sig'
                )
                output_files['total_consumo'] = {
                    'name': total_consumo_file_name,
                    'content': total_consumo_csv.encode('utf-8-sig')
                }
            
            return output_files
            
        except Exception as e:
            st.error(f"❌ Error al generar archivos de salida: {str(e)}")
            return {}
