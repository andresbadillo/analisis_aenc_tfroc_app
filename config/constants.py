"""Módulo para las constantes de la aplicación de análisis AENC y TFROC."""

# Configuración de la página
PAGE_CONFIG = {
    "page_title": "Análisis AENC y TFROC - Ruitoque",
    "page_icon": "assets/Isotipo.png",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "menu_items": None
}

# Estado inicial de la sesión
INITIAL_SESSION_STATE = {
    'ftp_connected': False,
    'sharepoint_connected': False,
    'files_downloaded': False,
    'files_processed': False,
    'annual_consumption_updated': False,  # Nuevo estado para el Paso 4
    'current_step': 1,
    'error_message': None,
    'success_message': None,
    'download_progress': 0,
    'processing_progress': 0
}

# Configuración FTP
FTP_CONFIG = {
    'server': 'xmftps.xm.com.co',
    'port': 210,
    'user': 'ISAMDNT\\1098742265',
    'password': 'Ru1t0qu309p2026.*'
}

# Configuración SharePoint (actualizada para Microsoft Graph API)
SHAREPOINT_CONFIG = {
    'url': 'https://ruitoqueesp1.sharepoint.com',
    'site': 'fronterascomerciales',
    # Nota: Las credenciales ahora se manejan a través de Azure AD
}

# Mapeo de OR (Operador de Red)
OR_MAPPING = {
    "CUNM": "ENEL",
    "SOLM": "AIRE",
    "SANM": "ESSA",
    "MARM": "AFINIA",
    "NSAM": "ESSA",
    "BOYM": "EBSA",
    "CASM": "ENERCA",
    "METM": "EMSA",
    "QUIM": "EDEQ",
    "RUIM": "RUITOQUE",
    "CHOM": "DISPAC",
    "CLOM": "EMCALI"
}

# Prioridad de versiones de archivos
FILE_VERSION_PRIORITY = [".TxF", ".TxR", ".Tx2"]

# Días de la semana en español
DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# Tipos de día
TIPOS_DIA = ["Hábil", "Hábil", "Hábil", "Hábil", "Hábil", "Sábado", "Domingo"]

# Colores para la interfaz
COLORS = {
    'primary': '#64B43F',
    'secondary': '#FF4B4B',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'info': '#17a2b8'
}
