"""
Configuración para Azure Active Directory.
Este archivo lee las variables de entorno desde el archivo .env
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de Azure AD
AZURE_CONFIG = {
    # Información del tenant
    'tenant_id': os.getenv('AZURE_TENANT_ID', 'YOUR_TENANT_ID'),
    
    # Información de la aplicación registrada
    'client_id': os.getenv('AZURE_CLIENT_ID', 'YOUR_CLIENT_ID'),
    'client_secret': os.getenv('AZURE_CLIENT_SECRET', 'YOUR_CLIENT_SECRET'),
    
    # URLs de redirección
    'redirect_uri': os.getenv('AZURE_REDIRECT_URI', 'http://localhost:8501'),
    
    # Permisos requeridos
    'scopes': [
        'https://graph.microsoft.com/User.Read',
        'https://graph.microsoft.com/Files.Read.All',
        'https://graph.microsoft.com/Files.ReadWrite.All',
        'https://graph.microsoft.com/Sites.Read.All',
        'https://graph.microsoft.com/Sites.ReadWrite.All'
    ],
    
    # Configuración de SharePoint
    'sharepoint_site_id': os.getenv('AZURE_SHAREPOINT_SITE_ID', 'YOUR_SHAREPOINT_SITE_ID'),
    'sharepoint_drive_id': os.getenv('AZURE_SHAREPOINT_DRIVE_ID', 'YOUR_SHAREPOINT_DRIVE_ID'),
}

# Configuración de autenticación
AUTH_CONFIG = {
    'authority': f"https://login.microsoftonline.com/{AZURE_CONFIG['tenant_id']}",
    'cache_location': 'localStorage',
    'navigate_to_login_request_url': False,
}

# Función para verificar si la configuración está completa
def is_azure_config_complete():
    """
    Verifica si todas las variables de Azure AD están configuradas.
    
    Returns:
        bool: True si todas las variables están configuradas, False en caso contrario
    """
    required_vars = [
        'AZURE_TENANT_ID',
        'AZURE_CLIENT_ID', 
        'AZURE_CLIENT_SECRET',
        'AZURE_REDIRECT_URI'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ Variables de Azure AD faltantes: {', '.join(missing_vars)}")
        return False
    
    return True

# Notas de configuración
"""
INSTRUCCIONES PARA CONFIGURAR AZURE AD:

1. Crear archivo .env en la raíz del proyecto con las siguientes variables:
   AZURE_TENANT_ID=tu_tenant_id
   AZURE_CLIENT_ID=tu_client_id
   AZURE_CLIENT_SECRET=tu_client_secret
   AZURE_REDIRECT_URI=http://localhost:8501
   AZURE_SHAREPOINT_SITE_ID=tu_site_id (opcional)
   AZURE_SHAREPOINT_DRIVE_ID=tu_drive_id (opcional)

2. Registrar la aplicación en Azure Portal:
   - Ir a Azure Portal > Azure Active Directory > Registros de aplicaciones
   - Crear nuevo registro
   - Nombre: "Análisis AENC TFROC - RUITOQUE"
   - Tipo de cuenta: "Solo las cuentas de este directorio organizativo"
   - URI de redirección: http://localhost:8501 (desarrollo) o URL de producción

3. Obtener información de la aplicación:
   - Client ID: Copiar del registro de la aplicación
   - Tenant ID: Copiar del registro de la aplicación
   - Client Secret: Crear un nuevo secreto en "Certificados y secretos"

4. Configurar permisos:
   - Ir a "Permisos de API"
   - Agregar permisos de Microsoft Graph:
     * User.Read
     * Files.Read.All
     * Files.ReadWrite.All
     * Sites.Read.All
     * Sites.ReadWrite.All
   - Conceder consentimiento de administrador

5. Para producción, cambiar AZURE_REDIRECT_URI a la URL de la aplicación desplegada
"""
