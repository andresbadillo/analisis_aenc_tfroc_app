# Análisis AENC y TFROC - RUITOQUE E.S.P

Aplicación Streamlit para el análisis y procesamiento de archivos AENC y TFROC desde el servidor FTP de XM hacia SharePoint.

## 📋 Descripción

Esta aplicación automatiza el proceso de descarga, procesamiento y carga de archivos AENC (Análisis de Energía) y TFROC (Tarifas de Frontera) desde el servidor FTP de XM hacia SharePoint, siguiendo un flujo de trabajo estructurado en 4 pasos principales.

## 🚀 Características

- **Descarga automática** de archivos desde FTP de XM
- **Procesamiento inteligente** con priorización de versiones (.TxF > .TxR > .Tx2)
- **Carga a SharePoint** con limpieza automática de archivos
- **Procesamiento de datos** con transformaciones y cálculos
- **Actualización automática** del archivo de consumo anual
- **Interfaz intuitiva** con seguimiento de progreso en tiempo real
- **Manejo de errores** robusto con mensajes informativos

## 📁 Estructura del Proyecto

```
analisis_aenc_tfroc_app/
├── app.py                          # Aplicación principal
├── requirements.txt                # Dependencias
├── .env                           # Variables de entorno (crear manualmente)
├── .gitignore                     # Archivos a ignorar en Git
├── README.md                      # Documentación
├── MANUAL_USUARIO.md              # Manual de usuario
├── DEPLOYMENT.md                  # Guía de despliegue
├── AZURE_AD_SETUP.md              # Configuración de Azure AD
├── config/                        # Configuración
│   ├── constants.py               # Constantes de la aplicación
│   ├── styles.py                  # Estilos CSS
│   └── azure_config.py            # Configuración de Azure AD
├── auth/                          # Autenticación
│   ├── __init__.py                # Inicializador del módulo auth
│   ├── azure_auth.py              # Autenticación con Azure AD
│   └── sharepoint.py              # Cliente SharePoint con Microsoft Graph API
├── utils/                         # Utilidades
│   ├── ftp_client.py             # Cliente FTP
│   ├── data_processor.py         # Procesador de datos
│   └── annual_consumption_updater.py # Actualizador de consumo anual
└── assets/                        # Recursos
    ├── Logo1.png                 # Logo principal
    └── path1310.png              # Logo sidebar
```

## 🛠️ Instalación

### Prerrequisitos

- Python 3.8 o superior
- Acceso al servidor FTP de XM
- Acceso a SharePoint de RUITOQUE

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

### Configuración

1. **Configuración FTP**: Los datos de conexión están en `config/constants.py`
2. **Configuración SharePoint**: Los datos de conexión están en `config/constants.py`
3. **Configuración Azure AD**: 
   - Crear archivo `.env` en la raíz del proyecto
   - Completar las variables de Azure AD en el archivo `.env`
   - Ver `AZURE_AD_SETUP.md` para instrucciones detalladas
4. **Assets**: Colocar los logos en la carpeta `assets/`

### Autenticación

La aplicación utiliza autenticación con Azure Active Directory:

- **Flujo de autenticación**: OAuth 2.0 con Azure AD
- **Componente**: `streamlit-oauth` para la interfaz de autenticación
- **API**: Microsoft Graph API para operaciones de SharePoint
- **Seguridad**: Tokens de acceso temporales, sin almacenamiento local de credenciales

## 🎯 Uso

### Ejecutar la aplicación

```bash
streamlit run app.py
```

### Flujo de trabajo

La aplicación se ejecuta en 4 pasos secuenciales:

#### Paso 1: Descargar archivos desde FTP
- Verifica si ya existen archivos .TxF en SharePoint
- Si no existen, conecta al servidor FTP de XM
- Descarga archivos AENC y TFROC del mes actual y anterior
- Prioriza versiones: .TxF > .TxR > .Tx2

#### Paso 2: Subir archivos a SharePoint
- Conecta a SharePoint
- Verifica si ya existen archivos .TxF
- Sube archivos descargados
- Limpia archivos según prioridad

#### Paso 3: Procesar datos AENC y TFROC
- Carga archivos desde SharePoint
- Procesa datos día a día
- Aplica transformaciones y cálculos
- Genera archivos CSV consolidados:
  - `aenc_consolidado_{mes}_{año}.csv`
  - `consumos_{mes}_{año}.csv`
  - `total_consumo_{mes}_{año}.csv`

#### Paso 4: Actualizar archivo de consumo anual
- Carga archivo de consumo anual
- Actualiza con datos del mes procesado
- Sube archivo actualizado

## 📊 Archivos Generados

### Archivos Mensuales
- **AENC Consolidado**: Datos AENC procesados con información de fecha, día y tipo de día
- **Consumos**: Datos unidos AENC + TFROC con cálculos aplicados
- **Total Consumo**: Resumen de consumo total por frontera

### Archivo Anual
- **Consumos Anual**: Archivo consolidado con todos los meses del año

## 🔧 Configuración

### Constantes principales

```python
# Configuración FTP
FTP_CONFIG = {
    'server': 'xmftps.xm.com.co',
    'port': 210,
    'user': 'ISAMDNT\\1098742265',
    'password': 'Ru1t0qu309p2026.'
}

# Configuración SharePoint
SHAREPOINT_CONFIG = {
    'url': 'https://ruitoqueesp1.sharepoint.com',
    'site': 'fronterascomerciales',
    'user': 'rbadillo@ruitoqueesp.com',
    'password': 'r2083502R'
}
```

### Mapeo de Operadores de Red

```python
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
```

### Configuración de Azure Active Directory

Para usar la autenticación con Azure AD, configurar las siguientes variables en el archivo `.env`:

```env
# Información del tenant de Azure AD
AZURE_TENANT_ID=your_tenant_id_here

# Información de la aplicación registrada en Azure
AZURE_CLIENT_ID=your_client_id_here
AZURE_CLIENT_SECRET=your_client_secret_here

# URL de redirección (desarrollo local)
AZURE_REDIRECT_URI=http://localhost:8501

# Configuración de SharePoint (opcional)
AZURE_SHAREPOINT_SITE_ID=your_sharepoint_site_id_here
AZURE_SHAREPOINT_DRIVE_ID=your_sharepoint_drive_id_here
```

**Pasos para configurar Azure AD:**

1. **Registrar la aplicación en Azure Portal**:
   - Ir a Azure Portal > Azure Active Directory > Registros de aplicaciones
   - Crear nuevo registro con nombre "Análisis AENC TFROC - RUITOQUE"
   - Configurar URI de redirección: `http://localhost:8501` (desarrollo)

2. **Obtener credenciales**:
   - Client ID: Copiar del registro de la aplicación
   - Tenant ID: Copiar del registro de la aplicación
   - Client Secret: Crear en "Certificados y secretos"

3. **Configurar permisos**:
   - Agregar permisos de Microsoft Graph:
     * User.Read
     * Files.Read.All
     * Files.ReadWrite.All
     * Sites.Read.All
     * Sites.ReadWrite.All
   - Conceder consentimiento de administrador

4. **Actualizar archivo .env** con los valores obtenidos

## 🚨 Solución de Problemas

### Error de conexión FTP
- Verificar credenciales en `config/constants.py`
- Comprobar conectividad de red
- Verificar que el servidor FTP esté disponible

### Error de conexión SharePoint
- Verificar credenciales en `config/constants.py`
- Comprobar permisos de acceso
- Verificar que la URL de SharePoint sea correcta

### Error de configuración Azure AD
- Verificar que el archivo `.env` existe en la raíz del proyecto
- Comprobar que todas las variables de Azure AD están configuradas
- Verificar que la aplicación esté registrada correctamente en Azure Portal
- Comprobar que los permisos de API estén configurados y concedidos

### Error de procesamiento de datos
- Verificar que los archivos tengan el formato esperado
- Comprobar que existan archivos AENC y TFROC correspondientes
- Verificar permisos de escritura en carpeta temporal

## 📝 Notas Técnicas

### Priorización de archivos
La aplicación sigue esta jerarquía para seleccionar archivos:
1. **.TxF** (Archivos finales)
2. **.TxR** (Archivos de revisión)
3. **.Tx2** (Archivos secundarios)

### Procesamiento de datos
- Los archivos se leen con encoding `latin1`
- Se aplica factor de pérdidas a los consumos horarios
- Se mapean niveles de tensión por rangos
- Se determinan tipos de día (Hábil, Sábado, Domingo, Festivo)

### Ubicaciones SharePoint
- **Archivos mensuales**: `Documentos Compartidos/aenc/{año}/{mes}/`
- **Archivo anual**: `Documentos Compartidos/aenc/fact_consumos/`

## 🤝 Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto es propiedad de RUITOQUE E.S.P.

## 📞 Soporte

Para soporte técnico o preguntas sobre la aplicación, contactar al equipo de desarrollo de RUITOQUE E.S.P.

---

**Versión**: 1.0  
**Última actualización**: 2025  
**Desarrollado por**: RUITOQUE E.S.P
