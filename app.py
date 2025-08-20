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



# --- PASO 1: DESCARGAR ARCHIVOS DESDE FTP ---
st.markdown("## 📥 Paso 1: Descargar archivos desde FTP")

with st.expander("🔍 Ver detalles del Paso 1", expanded=True):
    st.markdown("""
    **Lógica del proceso**:
    
    **PROCESO 1 (Mes anterior)**:
    1. Crea conexion al servidor FTP de XM
    2. Verificar archivos existentes en SharePoint para mes anterior
    3. Si existen archivos .TxF, no descargar del FTP
    4. Si no existen, proceder con la descarga de los archivos .TxF desde el FTP
    5. Primero busca archivos ".TxF". Si no hay ".TxF", busca ".TxR". Si no hay ".TxR", busca ".Tx2"
    6. Cerrar conexiones del proceso 1
    
    **PROCESO 2 (Mes actual)**:
    
    7. Crear nuevas conexiones independientes para SharePoint y FTP
    8. Siempre proceder con la descarga de los archivos aenc y tfroc del mes actual desde el FTP
    9. Cerrar conexiones del proceso 2
    
    **Archivos a descargar**:
    - Archivos AENC (con prioridad .TxF > .TxR > .Tx2)
    - Archivos TFROC (con prioridad .TxF > .TxR > .Tx2)
    
    **Ubicación FTP**: `/INFORMACION_XM/USUARIOSK/RTQC/sic/comercia/{año}-{mes}`
    **Ubicación SharePoint**: `Documentos/aenc/{año}/{mes}`
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
                    
                    # Variables para rastrear descargas
                    files_downloaded = False
                    
                    # ========================================
                    # PROCESO 1: MES ANTERIOR
                    # ========================================
                    st.subheader(f"📅 PROCESO 1: Mes anterior ({previous_month}/{previous_year})")
                    
                    # Crear nuevas instancias para el mes anterior
                    sharepoint_client_prev = SharePointClient(token)
                    ftp_client_prev = FTPClient()
                    
                    # Verificar archivos existentes para mes anterior (solo .TxF)
                    prev_files_exist = sharepoint_client_prev.verify_files_before_download(previous_year, previous_month)
                    
                    if not prev_files_exist:
                        # Conectar al FTP y descargar archivos del mes anterior
                        if ftp_client_prev.connect():
                            st.session_state['ftp_connected'] = True
                            prev_files = ftp_client_prev.download_month_files(previous_year, previous_month)
                            
                            # Cerrar conexión FTP del mes anterior
                            ftp_client_prev.disconnect()
                            
                            if prev_files:
                                st.success(f"✅ Descargados {len(prev_files)} archivos del mes anterior")
                                files_downloaded = True
                            else:
                                st.warning("⚠️ No se pudieron descargar archivos del mes anterior")
                        else:
                            st.error("❌ No se pudo conectar al servidor FTP para el mes anterior")
                            st.session_state['error_message'] = "Error de conexión FTP para mes anterior"
                            st.rerun()
                            st.stop()
                    else:
                        st.info(f"✅ Mes anterior {previous_month}/{previous_year}: Archivos .TxF ya existen en SharePoint")
                    
                    # ========================================
                    # PROCESO 2: MES ACTUAL
                    # ========================================
                    st.subheader(f"📅 PROCESO 2: Mes actual ({current_month}/{current_year})")
                    
                    # Crear nuevas instancias para el mes actual
                    sharepoint_client_current = SharePointClient(token)
                    ftp_client_current = FTPClient()
                    
                    # Siempre descargar archivos del mes actual desde FTP (sin verificar SharePoint)
                    try:
                        # Conectar al FTP para el mes actual
                        if ftp_client_current.connect():
                            st.session_state['ftp_connected'] = True
                            
                            # Llamar al método de descarga
                            current_files = ftp_client_current.download_month_files(current_year, current_month)
                            
                            # Cerrar conexión FTP del mes actual
                            ftp_client_current.disconnect()
                            
                            if current_files and len(current_files) > 0:
                                st.success(f"✅ Descargados {len(current_files)} archivos del mes actual")
                                files_downloaded = True
                            else:
                                st.warning("⚠️ No se pudieron descargar archivos del mes actual")
                        else:
                            st.error("❌ No se pudo conectar al servidor FTP para el mes actual")
                            st.session_state['error_message'] = "Error de conexión FTP para mes actual"
                            st.rerun()
                            st.stop()
                            
                    except Exception as e:
                        st.error(f"❌ Error durante la descarga del mes actual: {str(e)}")
                        st.session_state['error_message'] = f"Error en descarga del mes actual: {str(e)}"
                        st.rerun()
                        st.stop()
                    
                    # Verificar si se descargaron archivos antes de marcar como completado
                    if files_downloaded:
                        st.session_state['files_downloaded'] = True
                        st.session_state['success_message'] = "Paso 1 completado: Archivos descargados exitosamente"
                    else:
                        st.warning("⚠️ No se descargaron archivos nuevos. Verifica la configuración.")
                        st.session_state['files_downloaded'] = False
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
    
    **Ubicación SharePoint**: `Documentos/aenc/{año}/{mes}`
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
                    
                    # Procesar subida para mes anterior primero
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
    
    # Selectores de año y mes
    col1, col2 = st.columns(2)
    
    with col1:
        # Selector de año (últimos 5 años + año actual)
        current_year = datetime.now().year
        year_options = list(range(current_year - 4, current_year + 1))
        selected_year = st.selectbox(
            "📅 Seleccionar Año:",
            options=year_options,
            index=len(year_options) - 1,  # Por defecto año actual
            help="Selecciona el año para procesar los datos"
        )
    
    with col2:
        # Selector de mes
        month_options = [
            ("Enero", "01"), ("Febrero", "02"), ("Marzo", "03"), ("Abril", "04"),
            ("Mayo", "05"), ("Junio", "06"), ("Julio", "07"), ("Agosto", "08"),
            ("Septiembre", "09"), ("Octubre", "10"), ("Noviembre", "11"), ("Diciembre", "12")
        ]
        selected_month_name, selected_month = st.selectbox(
            "📅 Seleccionar Mes:",
            options=month_options,
            index=datetime.now().month - 1,  # Por defecto mes actual
            format_func=lambda x: x[0],  # Mostrar nombre del mes
            help="Selecciona el mes para procesar los datos"
        )
    
    # Mostrar información de selección
    st.info(f"📋 **Procesamiento seleccionado**: {selected_month_name} {selected_year}")
    
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
                    # Procesar el mes seleccionado
                    processed_data = data_processor.process_month_data(sharepoint_client, selected_year, selected_month)
                    
                    if processed_data:
                        # Generar archivos de salida
                        output_files = data_processor.generate_output_files(processed_data, selected_year, selected_month)
                        
                        if output_files:
                            # Subir archivos procesados
                            uploaded_count = 0
                            
                            for file_type, file_data in output_files.items():
                                if sharepoint_client.upload_processed_files(
                                    selected_year, selected_month, 
                                    file_data['content'], file_data['name']
                                ):
                                    uploaded_count += 1
                            
                            if uploaded_count == len(output_files):
                                st.session_state['files_processed'] = True
                                st.session_state['success_message'] = f"✅ Paso 3 completado: {selected_month_name} {selected_year} procesado exitosamente"
                            else:
                                st.session_state['error_message'] = f"Error: Solo se subieron {uploaded_count} de {len(output_files)} archivos"
                        else:
                            st.session_state['error_message'] = "Error: No se pudieron generar los archivos de salida"
                    else:
                        st.session_state['error_message'] = f"Error: No se pudieron procesar los datos para {selected_month_name} {selected_year}"
                else:
                    st.session_state['error_message'] = "Error: No se pudo conectar a SharePoint"
                
            except Exception as e:
                st.error(f"❌ Error en Paso 3: {str(e)}")
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
