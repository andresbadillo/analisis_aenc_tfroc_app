"""
Módulo para actualizar el archivo de consumo anual.
"""

import streamlit as st
import pandas as pd
import io
from datetime import datetime


class AnnualConsumptionUpdater:
    """
    Clase para actualizar el archivo de consumo anual.
    """
    
    def __init__(self):
        """Inicializa el actualizador de consumo anual."""
        pass
    
    def load_annual_file(self, sharepoint_client, year):
        """
        Carga el archivo de consumo anual desde SharePoint.
        
        Args:
            sharepoint_client: Cliente de SharePoint
            year (int): Año
            
        Returns:
            pd.DataFrame: DataFrame del archivo anual
        """
        try:
            # Obtener carpeta de fact_consumos
            folder_path = "aenc_pruebas/fact_consumos"
            files = sharepoint_client.list_files(folder_path)
            
            if not files:
                st.warning("⚠️ No se encontraron archivos en la carpeta fact_consumos")
                return None
            
            # Buscar archivo de consumo anual específico del año
            file_name = f"consumos_{year}.csv"
            annual_file = next((f for f in files if f['name'] == file_name), None)
            
            if not annual_file:
                st.warning(f"⚠️ No se encontró archivo de consumo anual: {file_name}")
                return None
            
            file_content = sharepoint_client.download_file_content(folder_path, annual_file['name'])
            
            if not file_content:
                return None
            
            # Leer el archivo CSV
            df = pd.read_csv(io.BytesIO(file_content), sep=",", encoding='utf-8-sig')
            
            st.info(f"📁 Archivo anual: {annual_file['name']} ({len(df)} registros)")
            return df
            
        except Exception as e:
            st.error(f"❌ Error al cargar archivo anual: {str(e)}")
            return None
    
    def load_monthly_file(self, sharepoint_client, year, month):
        """
        Carga el archivo de consumo mensual desde SharePoint.
        
        Args:
            sharepoint_client: Cliente de SharePoint
            year (int): Año
            month (str): Mes en formato MM
            
        Returns:
            pd.DataFrame: DataFrame del archivo mensual
        """
        try:
            # Obtener carpeta del mes
            folder_path = sharepoint_client.get_folder_path(year, month)
            files = sharepoint_client.list_files(folder_path)
            
            if not files:
                st.warning(f"⚠️ No se encontraron archivos en la carpeta {folder_path}")
                return None
            
            # Buscar archivo de consumos del mes
            monthly_files = [f for f in files if f['name'].startswith(f'consumos_{month}_{year}')]
            
            if not monthly_files:
                st.warning(f"⚠️ No se encontró archivo de consumos para {month}/{year}")
                return None
            
            monthly_file = monthly_files[0]
            file_content = sharepoint_client.download_file_content(folder_path, monthly_file['name'])
            
            if not file_content:
                return None
            
            # Leer el archivo CSV
            df = pd.read_csv(io.BytesIO(file_content), sep=",", encoding='utf-8-sig')
            
            st.info(f"📁 Archivo mensual: {monthly_file['name']} ({len(df)} registros)")
            return df
            
        except Exception as e:
            st.error(f"❌ Error al cargar archivo mensual: {str(e)}")
            return None
    
    def update_annual_consumption(self, sharepoint_client, year, month):
        """
        Actualiza el archivo de consumo anual con los datos del mes.
        
        Args:
            sharepoint_client: Cliente de SharePoint
            year (int): Año
            month (str): Mes en formato MM
            
        Returns:
            bool: True si la actualización es exitosa, False en caso contrario
        """
        try:
            # Cargar archivo anual
            annual_df = self.load_annual_file(sharepoint_client, year)
            if annual_df is None:
                return False
            
            # Cargar archivo mensual
            monthly_df = self.load_monthly_file(sharepoint_client, year, month)
            if monthly_df is None:
                return False
            
            # Convertir columnas de fecha a datetime
            annual_df['FECHA'] = pd.to_datetime(annual_df['FECHA'], format='%Y-%m-%d')
            monthly_df['FECHA'] = pd.to_datetime(monthly_df['FECHA'], format='%d-%m-%Y')
            
            # Filtrar datos del mes actual en el archivo anual
            annual_df = annual_df[~((annual_df['FECHA'].dt.year == year) & (annual_df['FECHA'].dt.month == int(month)))]
            
            # Concatenar datos
            updated_df = pd.concat([annual_df, monthly_df], ignore_index=True)
            
            # Ordenar por fecha y código de frontera
            updated_df = updated_df.sort_values(by=["FECHA", "CODIGO FRONTERA"])
            
            # Generar archivo CSV actualizado
            file_name = f"consumos_{year}.csv"
            csv_content = updated_df.to_csv(index=False, sep=",", encoding='utf-8-sig')
            
            # Subir archivo actualizado
            success = sharepoint_client.update_annual_consumption_file(
                year, month, csv_content.encode('utf-8-sig')
            )
            
            if success:
                st.info(f"📤 Archivo anual actualizado: {file_name} ({len(updated_df)} registros)")
                return True
            else:
                st.error("❌ Error al subir archivo anual actualizado")
                return False
                
        except Exception as e:
            st.error(f"❌ Error al actualizar consumo anual: {str(e)}")
            return False
