"""
Aplicación principal para el análisis de datos AENC y TFROC.
"""

import streamlit as st
import os
import shutil
from datetime import datetime
import warnings

from config.constants import PAGE_CONFIG, INITIAL_SESSION_STATE
from config.styles import CUSTOM_CSS
from config.azure_config import is_azure_config_complete
from utils.ftp_client import FTPClient
from utils.data_processor import DataProcessor
from utils.annual_consumption_updater import AnnualConsumptionUpdater
from auth.azure_auth import AzureAuth
from auth.sharepoint import SharePointClient

# Ignorar advertencias
warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(**PAGE_CONFIG)

# Aplicar estilos CSS personalizados
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Logo principal
col1, col2, col3 = st.columns([4, 2, 4])
with col2:
    st.image("assets/Logo1.png", width=200, use_container_width=True)
st.markdown("<br><br>", unsafe_allow_html=True)

# Título principal
st.markdown("<h1 class='titulo-principal'>Análisis AENC y TFROC</h1>", unsafe_allow_html=True)

# Inicializar el estado de la sesión
for key, value in INITIAL_SESSION_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Inicializar autenticación Azure AD
azure_auth = AzureAuth()

def reset_session():
    """Reinicia el estado de la sesión."""
    for key, value in INITIAL_SESSION_STATE.items():
        st.session_state[key] = value

def clean_temp_folder():
    """Limpia la carpeta temporal de archivos descargados."""
    temp_folder = "archivos_descargados"
    if os.path.exists(temp_folder):
        try:
            for filename in os.listdir(temp_folder):
                file_path = os.path.join(temp_folder, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            st.success("✅ Carpeta temporal limpiada exitosamente")
        except Exception as e:
            st.error(f"❌ Error al limpiar carpeta temporal: {str(e)}")

# --- SIDEBAR CON INFORMACIÓN ---
with st.sidebar:
    # Logo de la compañía centrado
    col1, col2, col3 = st.columns([0.5, 4, 0.5])
    with col2:
        st.image("assets/path1310.png", width=200)
    
    st.markdown("---")
    
    st.header("ℹ️ Información")
    st.markdown("""
    Esta aplicación permite descargar y procesar archivos AENC y TFROC desde el servidor FTP de XM
    y cargarlos en SharePoint para su análisis posterior.
    """)
    
    st.markdown("""
    ### Instrucciones
    1. **Paso 1**: Descargar archivos desde FTP
    2. **Paso 2**: Subir archivos a SharePoint
    3. **Paso 3**: Procesar datos AENC y TFROC
    4. **Paso 4**: Actualizar archivo de consumo anual
    
    ### Notas
    - Los archivos se procesan por prioridad: .TxF > .TxR > .Tx2
    - Se procesan automáticamente el mes actual y el mes anterior
    - Los archivos procesados se guardan en SharePoint
    """)
    
    st.markdown("---")
    
    st.header("🔧 Acciones")
    
    # Botón para limpiar carpeta temporal
    if st.button("🗑️ Limpiar archivos temporales"):
        clean_temp_folder()
    
    # Botón para reiniciar sesión
    if st.button("🔄 Reiniciar aplicación"):
        reset_session()
        st.rerun()
    
    st.markdown("---")
    
    st.header("📊 Estado actual")
    
    # Mostrar estado de las conexiones
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state['ftp_connected']:
            st.success("✅ FTP")
        else:
            st.error("❌ FTP")
    
    with col2:
        if st.session_state['sharepoint_connected']:
            st.success("✅ SharePoint")
        else:
            st.error("❌ SharePoint")
    
    # Mostrar estado de los archivos
    if st.session_state['files_downloaded']:
        st.success("✅ Archivos descargados")
    else:
        st.info("⏳ Archivos no descargados")
    
    if st.session_state['files_processed']:
        st.success("✅ Archivos procesados")
    else:
        st.info("⏳ Archivos no procesados")
    
    # Información de autenticación
    st.markdown("---")
    st.header("🔐 Estado de Autenticación")
    
    if azure_auth.is_authenticated():
        st.success("✅ Usuario autenticado")
        st.info("Sesión activa con Azure AD")
        
        # Botón para cerrar sesión
        if st.button("🚪 Cerrar sesión"):
            azure_auth.logout()
    else:
        st.error("❌ Usuario no autenticado")
        st.info("Inicia sesión para continuar")
    
    # Verificar configuración de Azure AD
    st.markdown("---")
    st.header("⚙️ Configuración Azure AD")
    
    if is_azure_config_complete():
        st.success("✅ Configuración Azure AD completa")
    else:
        st.error("❌ Configuración Azure AD incompleta")
        st.info("📝 Verificar archivo .env en la raíz del proyecto")

# --- VERIFICACIÓN DE AUTENTICACIÓN ---

# Verificar si el usuario está autenticado
if not azure_auth.is_authenticated():
    st.markdown("## 🔐 Autenticación Requerida")
    st.markdown("""
    Para acceder a la aplicación de análisis AENC y TFROC, debes iniciar sesión con tus credenciales de Ruitoque.
    
    **¿Por qué necesito autenticarme?**
    - La aplicación accede a SharePoint para verificar y subir archivos
    - Se requiere autenticación segura con Azure Active Directory
    - Tus credenciales están protegidas y no se almacenan localmente
    """)
    
    # Mostrar botón de autenticación
    token = azure_auth.authenticate()
    
    if not token:
        st.stop()
    
    # Si llegamos aquí, el usuario está autenticado
    st.success("✅ Autenticación exitosa")
    st.rerun()

# --- CONTENIDO PRINCIPAL ---

# Mostrar mensajes de error o éxito
if st.session_state['error_message']:
    st.error(f"❌ {st.session_state['error_message']}")
    st.session_state['error_message'] = None

if st.session_state['success_message']:
    st.success(f"✅ {st.session_state['success_message']}")
    st.session_state['success_message'] = None

# --- DIAGNÓSTICO INTEGRADO ---
st.markdown("## 🔍 Diagnóstico de Conexión")

with st.expander("🔧 Ejecutar diagnóstico de SharePoint", expanded=False):
    st.markdown("""
    **Diagnóstico integrado**: Este diagnóstico se ejecuta dentro de la aplicación principal 
    para poder acceder al token de autenticación y verificar la conexión a SharePoint.
    """)
    
    if st.button("🔍 Ejecutar Diagnóstico", type="secondary"):
        if azure_auth.is_authenticated():
            token = azure_auth.get_token()
            st.success("✅ Token de autenticación disponible")
            
            # Crear cliente SharePoint
            sharepoint_client = SharePointClient(token)
            
            # Ejecutar diagnóstico
            st.subheader("📋 Resultados del Diagnóstico")
            
            # Probar conexión
            st.write("**1. Prueba de conexión a SharePoint:**")
            if sharepoint_client.test_connection():
                st.success("✅ Conexión a SharePoint exitosa")
                
                # Verificar archivos existentes
                st.write("**2. Verificación de archivos existentes:**")
                current_year = datetime.now().year
                current_month = datetime.now().month
                
                # Obtener mes anterior
                ftp_client = FTPClient()
                previous_year, previous_month = ftp_client.get_previous_month(current_year, current_month)
                
                st.info(f"Verificando archivos para:")
                st.info(f"- Mes actual: {current_month}/{current_year}")
                st.info(f"- Mes anterior: {previous_month}/{previous_year}")
                
                # Verificar mes actual
                current_files_exist = sharepoint_client.verify_files_before_download(current_year, current_month)
                prev_files_exist = sharepoint_client.verify_files_before_download(previous_year, previous_month)
                
                st.write("**3. Resumen:**")
                if current_files_exist and prev_files_exist:
                    st.success("✅ Ambos meses tienen archivos .TxF en SharePoint")
                    st.info("No es necesario descargar archivos del FTP")
                elif current_files_exist or prev_files_exist:
                    st.warning("⚠️ Solo un mes tiene archivos .TxF en SharePoint")
                    st.info("Se necesitará descargar archivos del FTP para el mes faltante")
                else:
                    st.info("ℹ️ Ningún mes tiene archivos .TxF en SharePoint")
                    st.info("Se necesitará descargar archivos del FTP para ambos meses")
            else:
                st.error("❌ No se pudo conectar a SharePoint")
                st.info("💡 Verifica los permisos de la aplicación en Azure Portal")
        else:
            st.error("❌ No hay token de autenticación")
            st.info("💡 Primero inicia sesión con Azure AD")

# --- PASO 1: DESCARGAR ARCHIVOS DESDE FTP ---
st.markdown("## 📥 Paso 1: Descargar archivos desde FTP")

with st.expander("🔍 Ver detalles del Paso 1", expanded=True):
    st.markdown("""
    **Objetivo**: Verificar si ya existen archivos en SharePoint, y si no existen, 
    conectar al servidor FTP de XM y descargar los archivos AENC y TFROC del mes actual y del mes anterior.
    
    **Lógica del proceso**:
    1. Verificar si ya existen archivos .TxF en SharePoint para el mes actual y anterior
    2. Si existen archivos, no descargar del FTP
    3. Si no existen, proceder con la descarga del FTP
    
    **Archivos a descargar**:
    - Archivos AENC (con prioridad .TxF > .TxR > .Tx2)
    - Archivos TFROC (con prioridad .TxF > .TxR > .Tx2)
    
    **Ubicación FTP**: `/INFORMACION_XM/USUARIOSK/RTQC/sic/comercia/{año}-{mes}`
    **Ubicación SharePoint**: `Documentos Compartidos/aenc/{año}/{mes}`
    """)
    
    if st.button("🚀 Ejecutar Paso 1: Descargar archivos", 
                disabled=st.session_state['files_downloaded'],
                type="primary"):
        
        with st.spinner("🔄 Verificando archivos en SharePoint..."):
            try:
                # Obtener token de autenticación
                token = azure_auth.get_token()
                if not token:
                    st.error("❌ No hay token de autenticación válido")
                    st.session_state['error_message'] = "Error de autenticación"
                    st.rerun()
                    st.stop()
                
                # Crear cliente SharePoint con autenticación
                sharepoint_client = SharePointClient(token)
                
                # Probar conexión a SharePoint
                if sharepoint_client.test_connection():
                    st.success("✅ Conexión SharePoint establecida")
                    
                    # Obtener fechas actuales
                    current_year = datetime.now().year
                    current_month = datetime.now().month
                    
                    # Obtener mes anterior
                    ftp_client = FTPClient()
                    previous_year, previous_month = ftp_client.get_previous_month(current_year, current_month)
                    
                    # Verificar archivos existentes
                    st.info("🔍 Verificando archivos existentes en SharePoint...")
                    current_files_exist = sharepoint_client.verify_files_before_download(current_year, current_month)
                    prev_files_exist = sharepoint_client.verify_files_before_download(previous_year, previous_month)
                    
                    # Si ambos meses ya tienen archivos, no proceder con la descarga
                    if current_files_exist and prev_files_exist:
                        st.warning("⚠️ Los archivos ya existen en SharePoint para ambos meses")
                        st.info("No es necesario descargar archivos del FTP")
                        st.session_state['ftp_connected'] = True
                        st.session_state['files_downloaded'] = True
                        st.session_state['success_message'] = "Paso 1 completado: Archivos ya existen en SharePoint"
                        st.rerun()
                        st.stop()
                    
                    # Si al menos un mes necesita archivos, proceder con la descarga
                    st.info("🔄 Procediendo con la descarga del FTP...")
                    
                    # Conectar al FTP
                    if ftp_client.connect():
                        st.session_state['ftp_connected'] = True
                        st.success("✅ Conexión FTP establecida")
                        
                        # Procesar mes actual y anterior
                        results = ftp_client.process_current_and_previous_month()
                        
                        # Verificar si se descargaron archivos
                        total_files = sum(len(files) for files in results.values())
                        if total_files > 0:
                            st.session_state['files_downloaded'] = True
                            st.session_state['success_message'] = f"Paso 1 completado: {total_files} archivos descargados"
                        else:
                            st.session_state['error_message'] = "No se pudieron descargar archivos"
                    else:
                        st.session_state['error_message'] = "No se pudo conectar al servidor FTP"
                    
                    # Cerrar conexión FTP
                    ftp_client.disconnect()
                else:
                    st.session_state['error_message'] = "No se pudo conectar a SharePoint"
                
            except Exception as e:
                st.session_state['error_message'] = f"Error en Paso 1: {str(e)}"
        
        st.rerun()

# --- PASO 2: SUBIR ARCHIVOS A SHAREPOINT ---
st.markdown("## 📤 Paso 2: Subir archivos a SharePoint")

with st.expander("🔍 Ver detalles del Paso 2", expanded=True):
    st.markdown("""
    **Objetivo**: Conectar a SharePoint y subir los archivos descargados del FTP.
    
    **Proceso**:
    1. Verificar si ya existen archivos .TxF en SharePoint
    2. Subir archivos descargados
    3. Limpiar archivos según prioridad (.TxF > .TxR > .Tx2)
    
    **Ubicación SharePoint**: `Documentos Compartidos/aenc/{año}/{mes}`
    """)
    
    if st.button("🚀 Ejecutar Paso 2: Subir archivos", 
                disabled=not st.session_state['files_downloaded'] or st.session_state['sharepoint_connected'],
                type="primary"):
        
        with st.spinner("🔄 Ejecutando Paso 2..."):
            try:
                # Obtener token de autenticación
                token = azure_auth.get_token()
                if not token:
                    st.error("❌ No hay token de autenticación válido")
                    st.session_state['error_message'] = "Error de autenticación"
                    st.rerun()
                    st.stop()
                
                # Crear cliente SharePoint con autenticación
                sharepoint_client = SharePointClient(token)
                
                # Probar conexión a SharePoint
                if sharepoint_client.test_connection():
                    st.session_state['sharepoint_connected'] = True
                    
                    # Obtener año y mes actual
                    current_year = datetime.now().year
                    current_month = f"{datetime.now().month:02d}"
                    
                    # Obtener mes anterior
                    ftp_client = FTPClient()
                    previous_year, previous_month = ftp_client.get_previous_month(current_year, int(current_month))
                    
                    # Procesar subida para mes anterior
                    st.subheader(f"📅 Procesando mes anterior: {previous_month}/{previous_year}")
                    success_previous = sharepoint_client.process_month_upload(previous_year, previous_month)
                    
                    # Procesar subida para mes actual
                    st.subheader(f"📅 Procesando mes actual: {current_month}/{current_year}")
                    success_current = sharepoint_client.process_month_upload(current_year, current_month)
                    
                    if success_previous and success_current:
                        st.session_state['success_message'] = "Paso 2 completado: Archivos subidos exitosamente"
                    else:
                        st.session_state['error_message'] = "Error al subir algunos archivos"
                else:
                    st.session_state['error_message'] = "No se pudo conectar a SharePoint"
                
            except Exception as e:
                st.session_state['error_message'] = f"Error en Paso 2: {str(e)}"
        
        st.rerun()

# --- PASO 3: PROCESAR DATOS AENC Y TFROC ---
st.markdown("## 🔄 Paso 3: Procesar datos AENC y TFROC")

with st.expander("🔍 Ver detalles del Paso 3", expanded=True):
    st.markdown("""
    **Objetivo**: Procesar los archivos AENC y TFROC para generar reportes consolidados.
    
    **Proceso**:
    1. Cargar archivos desde SharePoint
    2. Procesar datos día a día
    3. Aplicar transformaciones y cálculos
    4. Generar archivos CSV consolidados
    
    **Archivos generados**:
    - `aenc_consolidado_{mes}_{año}.csv`
    - `consumos_{mes}_{año}.csv`
    - `total_consumo_{mes}_{año}.csv`
    """)
    
    if st.button("🚀 Ejecutar Paso 3: Procesar datos", 
                disabled=not st.session_state['sharepoint_connected'] or st.session_state['files_processed'],
                type="primary"):
        
        with st.spinner("🔄 Ejecutando Paso 3..."):
            try:
                # Obtener token de autenticación
                token = azure_auth.get_token()
                if not token:
                    st.error("❌ No hay token de autenticación válido")
                    st.session_state['error_message'] = "Error de autenticación"
                    st.rerun()
                    st.stop()
                
                # Inicializar clientes
                sharepoint_client = SharePointClient(token)
                data_processor = DataProcessor()
                
                # Probar conexión a SharePoint
                if sharepoint_client.test_connection():
                    # Obtener año y mes actual
                    current_year = datetime.now().year
                    current_month = f"{datetime.now().month:02d}"
                    
                    # Obtener mes anterior
                    ftp_client = FTPClient()
                    previous_year, previous_month = ftp_client.get_previous_month(current_year, int(current_month))
                    
                    # Procesar mes anterior
                    st.subheader(f"📅 Procesando mes anterior: {previous_month}/{previous_year}")
                    processed_previous = data_processor.process_month_data(sharepoint_client, previous_year, previous_month)
                    
                    if processed_previous:
                        # Generar archivos de salida para mes anterior
                        output_files_previous = data_processor.generate_output_files(processed_previous, previous_year, previous_month)
                        
                        # Subir archivos procesados
                        for file_type, file_data in output_files_previous.items():
                            sharepoint_client.upload_processed_files(
                                previous_year, previous_month, 
                                file_data['content'], file_data['name']
                            )
                    
                    # Procesar mes actual
                    st.subheader(f"📅 Procesando mes actual: {current_month}/{current_year}")
                    processed_current = data_processor.process_month_data(sharepoint_client, current_year, current_month)
                    
                    if processed_current:
                        # Generar archivos de salida para mes actual
                        output_files_current = data_processor.generate_output_files(processed_current, current_year, current_month)
                        
                        # Subir archivos procesados
                        for file_type, file_data in output_files_current.items():
                            sharepoint_client.upload_processed_files(
                                current_year, current_month, 
                                file_data['content'], file_data['name']
                            )
                    
                    if processed_previous and processed_current:
                        st.session_state['files_processed'] = True
                        st.session_state['success_message'] = "Paso 3 completado: Datos procesados exitosamente"
                    else:
                        st.session_state['error_message'] = "Error al procesar algunos datos"
                else:
                    st.session_state['error_message'] = "No se pudo conectar a SharePoint"
                
            except Exception as e:
                st.session_state['error_message'] = f"Error en Paso 3: {str(e)}"
        
        st.rerun()

# --- PASO 4: ACTUALIZAR ARCHIVO DE CONSUMO ANUAL ---
st.markdown("## 📊 Paso 4: Actualizar archivo de consumo anual")

with st.expander("🔍 Ver detalles del Paso 4", expanded=True):
    st.markdown("""
    **Objetivo**: Actualizar el archivo de consumo anual con los datos del mes procesado.
    
    **Proceso**:
    1. Cargar archivo de consumo anual desde SharePoint
    2. Cargar archivo de consumos del mes procesado
    3. Eliminar datos del mes actual del archivo anual
    4. Concatenar datos actualizados
    5. Subir archivo actualizado
    
    **Ubicación**: `Documentos Compartidos/aenc/fact_consumos/consumos_{año}.csv`
    """)
    
    if st.button("🚀 Ejecutar Paso 4: Actualizar consumo anual", 
                disabled=not st.session_state['files_processed'],
                type="primary"):
        
        with st.spinner("🔄 Ejecutando Paso 4..."):
            try:
                # Obtener token de autenticación
                token = azure_auth.get_token()
                if not token:
                    st.error("❌ No hay token de autenticación válido")
                    st.session_state['error_message'] = "Error de autenticación"
                    st.rerun()
                    st.stop()
                
                # Inicializar clientes
                sharepoint_client = SharePointClient(token)
                annual_updater = AnnualConsumptionUpdater()
                
                # Probar conexión a SharePoint
                if sharepoint_client.test_connection():
                    # Obtener año y mes actual
                    current_year = datetime.now().year
                    current_month = f"{datetime.now().month:02d}"
                    
                    # Actualizar archivo de consumo anual
                    success = annual_updater.update_annual_consumption(sharepoint_client, current_year, current_month)
                    
                    if success:
                        st.session_state['success_message'] = "Paso 4 completado: Archivo anual actualizado exitosamente"
                    else:
                        st.session_state['error_message'] = "Error al actualizar archivo anual"
                else:
                    st.session_state['error_message'] = "No se pudo conectar a SharePoint"
                
            except Exception as e:
                st.session_state['error_message'] = f"Error en Paso 4: {str(e)}"
        
        st.rerun()

# --- RESUMEN FINAL ---
if st.session_state['files_processed']:
    st.markdown("## 🎉 Proceso Completado")
    
    st.success("""
    ✅ **¡Todos los pasos han sido completados exitosamente!**
    
    **Resumen de lo realizado**:
    - ✅ Archivos descargados desde FTP
    - ✅ Archivos subidos a SharePoint
    - ✅ Datos procesados y consolidados
    - ✅ Archivo de consumo anual actualizado
    
    Los archivos procesados están disponibles en SharePoint en las siguientes ubicaciones:
    - `Documentos Compartidos/aenc/{año}/{mes}/` - Archivos mensuales
    - `Documentos Compartidos/aenc/fact_consumos/` - Archivo anual consolidado
    """)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>Desarrollado por RUITOQUE E.S.P | Análisis AENC y TFROC</p>
    <p>Versión 1.0 | Última actualización: 2025</p>
</div>
""", unsafe_allow_html=True)
