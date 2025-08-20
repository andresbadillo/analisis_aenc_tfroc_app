# Guía de Despliegue - Análisis AENC y TFROC

## 🚀 Despliegue en Producción

### Prerrequisitos

1. **Servidor con Python 3.8+**
2. **Acceso a Azure Portal** para configurar la aplicación
3. **Permisos de administrador** en el tenant de Azure AD
4. **Acceso al servidor FTP** de XM
5. **Acceso a SharePoint** de RUITOQUE

### Paso 1: Preparar el servidor

#### Instalar dependencias del sistema
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx

# CentOS/RHEL
sudo yum install python3 python3-pip nginx

# Windows
# Instalar Python 3.8+ desde python.org
# Instalar IIS o usar servidor integrado de Streamlit
```

#### Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

#### Instalar dependencias Python
```bash
pip install -r requirements.txt
```

### Paso 2: Configurar Azure Active Directory

#### 1. Registrar la aplicación en Azure Portal

1. Ir a [Azure Portal](https://portal.azure.com)
2. Navegar a **Azure Active Directory** > **Registros de aplicaciones**
3. Hacer clic en **Nuevo registro**
4. Configurar:
   - **Nombre**: `Análisis AENC TFROC - RUITOQUE`
   - **Tipo de cuenta**: `Solo las cuentas de este directorio organizativo`
   - **URI de redirección**: `https://tu-dominio.com` (URL de producción)

#### 2. Obtener información de la aplicación

1. **Client ID**: Copiar del registro de la aplicación
2. **Tenant ID**: Copiar del registro de la aplicación
3. **Client Secret**: 
   - Ir a **Certificados y secretos**
   - Crear nuevo secreto de cliente
   - Copiar el valor (solo se muestra una vez)

#### 3. Configurar permisos de API

1. Ir a **Permisos de API**
2. Hacer clic en **Agregar un permiso**
3. Seleccionar **Microsoft Graph**
4. Agregar permisos delegados:
   - `User.Read`
   - `Files.Read.All`
   - `Files.ReadWrite.All`
   - `Sites.Read.All`
   - `Sites.ReadWrite.All`
5. Hacer clic en **Conceder consentimiento de administrador**

#### 4. Obtener información de SharePoint

Usar [Microsoft Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer) para obtener:

1. **Site ID**:
   ```
   GET https://graph.microsoft.com/v1.0/sites/ruitoqueesp1.sharepoint.com:/sites/fronterascomerciales
   ```

2. **Drive ID**:
   ```
   GET https://graph.microsoft.com/v1.0/sites/{site-id}/drives
   ```

### Paso 3: Configurar la aplicación

#### 1. Actualizar configuración de Azure

Editar `config/azure_config.py`:
```python
AZURE_CONFIG = {
    'tenant_id': 'TU_TENANT_ID',
    'client_id': 'TU_CLIENT_ID',
    'client_secret': 'TU_CLIENT_SECRET',
    'redirect_uri': 'https://tu-dominio.com',
    'sharepoint_site_id': 'TU_SITE_ID',
    'sharepoint_drive_id': 'TU_DRIVE_ID',
    # ... resto de configuración
}
```

#### 2. Verificar configuración FTP y SharePoint

Verificar en `config/constants.py`:
```python
FTP_CONFIG = {
    'server': 'xmftps.xm.com.co',
    'port': 210,
    'user': 'ISAMDNT\\1098742265',
    'password': 'Ru1t0qu309p2026.'
}

SHAREPOINT_CONFIG = {
    'url': 'https://ruitoqueesp1.sharepoint.com',
    'site': 'fronterascomerciales',
    'user': 'rbadillo@ruitoqueesp.com',
    'password': 'r2083502R'
}
```

#### 3. Configurar assets

Colocar los logos en la carpeta `assets/`:
- `Logo1.png` - Logo principal
- `path1310.png` - Logo del sidebar

### Paso 4: Configurar servidor web (Opcional)

#### Configuración con Nginx (Linux)

1. **Crear archivo de configuración Nginx**:
```bash
sudo nano /etc/nginx/sites-available/aenc-tfroc-app
```

2. **Contenido del archivo**:
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

3. **Habilitar el sitio**:
```bash
sudo ln -s /etc/nginx/sites-available/aenc-tfroc-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Configuración con IIS (Windows)

1. Instalar IIS y URL Rewrite Module
2. Crear sitio web en IIS
3. Configurar reverse proxy para redirigir a `http://localhost:8501`

### Paso 5: Configurar servicio del sistema

#### Linux (systemd)

1. **Crear archivo de servicio**:
```bash
sudo nano /etc/systemd/system/aenc-tfroc-app.service
```

2. **Contenido del archivo**:
```ini
[Unit]
Description=Análisis AENC TFROC App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/ruta/a/tu/aplicacion
Environment=PATH=/ruta/a/tu/aplicacion/venv/bin
ExecStart=/ruta/a/tu/aplicacion/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. **Habilitar y iniciar el servicio**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable aenc-tfroc-app
sudo systemctl start aenc-tfroc-app
sudo systemctl status aenc-tfroc-app
```

#### Windows (Task Scheduler)

1. Crear tarea programada para ejecutar:
```cmd
cd /d C:\ruta\a\tu\aplicacion
venv\Scripts\activate
streamlit run app.py --server.port 8501
```

### Paso 6: Configurar SSL/HTTPS

#### Con Let's Encrypt (Linux)

1. **Instalar Certbot**:
```bash
sudo apt install certbot python3-certbot-nginx
```

2. **Obtener certificado**:
```bash
sudo certbot --nginx -d tu-dominio.com
```

3. **Configurar renovación automática**:
```bash
sudo crontab -e
# Agregar línea:
0 12 * * * /usr/bin/certbot renew --quiet
```

### Paso 7: Configurar firewall

#### Linux (UFW)
```bash
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 22
sudo ufw enable
```

#### Windows Firewall
- Permitir puertos 80 y 443
- Permitir conexiones entrantes para la aplicación

### Paso 8: Monitoreo y logs

#### Configurar logs de Streamlit

Editar `streamlit.toml`:
```toml
[logger]
level = "info"
messageFormat = "%(asctime)s %(message)s"

[server]
logLevel = "info"
```

#### Configurar rotación de logs

```bash
# Crear script de rotación
sudo nano /etc/logrotate.d/aenc-tfroc-app

# Contenido:
/ruta/a/tu/aplicacion/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
}
```

### Paso 9: Pruebas de funcionamiento

#### Verificar acceso
1. Abrir navegador y navegar a `https://tu-dominio.com`
2. Verificar que la aplicación se carga correctamente
3. Probar autenticación con Azure AD
4. Ejecutar un paso de prueba

#### Verificar logs
```bash
# Ver logs del servicio
sudo journalctl -u aenc-tfroc-app -f

# Ver logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Paso 10: Backup y mantenimiento

#### Script de backup
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/aenc-tfroc-app"
APP_DIR="/ruta/a/tu/aplicacion"

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/app_backup_$DATE.tar.gz $APP_DIR
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

#### Programar backup
```bash
# Agregar a crontab
0 2 * * * /ruta/a/backup.sh
```

## 🔧 Configuración de Desarrollo

### Entorno local
```bash
# Clonar repositorio
git clone <url-del-repositorio>
cd analisis_aenc_tfroc_app

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run app.py
```

### Variables de entorno
Crear archivo `.env`:
```env
# Configuración de Azure AD
AZURE_TENANT_ID=tu_tenant_id
AZURE_CLIENT_ID=tu_client_id
AZURE_CLIENT_SECRET=tu_client_secret
AZURE_REDIRECT_URI=https://tu-dominio.com

# Configuración de SharePoint (opcional)
AZURE_SHAREPOINT_SITE_ID=tu_site_id
AZURE_SHAREPOINT_DRIVE_ID=tu_drive_id
```

**Nota**: Para producción, cambiar `AZURE_REDIRECT_URI` a la URL de la aplicación desplegada.

## 🚨 Solución de Problemas

### Error de conexión Azure AD
- Verificar configuración en `config/azure_config.py`
- Comprobar que la aplicación esté registrada correctamente
- Verificar permisos de API

### Error de conexión FTP
- Verificar credenciales en `config/constants.py`
- Comprobar conectividad de red
- Verificar que el servidor FTP esté disponible

### Error de conexión SharePoint
- Verificar credenciales en `config/constants.py`
- Comprobar permisos de acceso
- Verificar Site ID y Drive ID

### Error de permisos
- Verificar que el usuario tenga permisos de escritura
- Comprobar permisos de la carpeta de logs
- Verificar permisos de la carpeta temporal

## 📞 Soporte

Para soporte técnico durante el despliegue:
- **Equipo**: Desarrollo RUITOQUE E.S.P
- **Email**: [correo de soporte]
- **Documentación**: [enlace a documentación]

---

**Versión**: 1.0  
**Última actualización**: 2025  
**Aplicación**: Análisis AENC y TFROC - RUITOQUE E.S.P
