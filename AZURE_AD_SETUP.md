# 🔐 Configuración de Azure Active Directory

## 📋 Resumen del Problema

La aplicación está experimentando un error `403 Forbidden` al intentar conectarse a SharePoint. El diagnóstico muestra que:

1. ✅ **Azure AD está configurado** en el archivo `.env`
2. ❌ **La aplicación no está registrada** correctamente en Azure AD
3. ❌ **Faltan permisos** para acceder a SharePoint

## 🔧 Solución: Configurar Azure AD Correctamente

### Paso 1: Registrar la Aplicación en Azure Portal

1. **Acceder a Azure Portal**:
   - Ir a [portal.azure.com](https://portal.azure.com)
   - Iniciar sesión con la cuenta de administrador de RUITOQUE E.S.P

2. **Navegar a Azure Active Directory**:
   - Buscar "Azure Active Directory" en la barra de búsqueda
   - Hacer clic en "Azure Active Directory"

3. **Registrar nueva aplicación**:
   - En el menú lateral, hacer clic en "Registros de aplicaciones"
   - Hacer clic en "Nuevo registro"
   - Completar la información:
     - **Nombre**: `Análisis AENC TFROC - RUITOQUE`
     - **Tipos de cuenta admitidos**: `Solo las cuentas de este directorio organizativo`
     - **URI de redirección**: `http://localhost:8501` (para desarrollo)

4. **Guardar el registro**:
   - Hacer clic en "Registrar"
   - Anotar el **ID de aplicación (Client ID)** y **ID de directorio (Tenant ID)**

### Paso 2: Configurar Permisos de API

1. **Ir a la aplicación registrada**:
   - En "Registros de aplicaciones", hacer clic en la aplicación creada

2. **Configurar permisos**:
   - En el menú lateral, hacer clic en "Permisos de API"
   - Hacer clic en "Agregar un permiso"
   - Seleccionar "Microsoft Graph"
   - Seleccionar "Permisos de aplicación"
   - Buscar y agregar los siguientes permisos:
     - `Sites.Read.All`
     - `Sites.ReadWrite.All`
     - `Files.Read.All`
     - `Files.ReadWrite.All`
     - `User.Read.All`

3. **Conceder consentimiento de administrador**:
   - Hacer clic en "Conceder consentimiento de administrador"
   - Confirmar la acción

### Paso 3: Crear Secret de Cliente

1. **Ir a Certificados y secretos**:
   - En el menú lateral de la aplicación, hacer clic en "Certificados y secretos"

2. **Crear nuevo secret**:
   - Hacer clic en "Nuevo secret de cliente"
   - Agregar descripción: `Análisis AENC TFROC Secret`
   - Seleccionar expiración (recomendado: 24 meses)
   - Hacer clic en "Agregar"

3. **Copiar el valor del secret**:
   - **IMPORTANTE**: Copiar inmediatamente el valor del secret
   - No se podrá ver de nuevo después de cerrar la página

### Paso 4: Actualizar Archivo .env

Actualizar el archivo `.env` con los valores correctos:

```env
# Configuración de Azure Active Directory
AZURE_TENANT_ID=tu_tenant_id_real
AZURE_CLIENT_ID=tu_client_id_real
AZURE_CLIENT_SECRET=tu_client_secret_real
AZURE_REDIRECT_URI=http://localhost:8501
```

### Paso 5: Verificar Configuración

Ejecutar el script de prueba:

```bash
python test_azure_ad.py
```

## 🚨 Problemas Comunes y Soluciones

### Error: "Application not found in directory"
**Causa**: La aplicación no está registrada en el tenant correcto
**Solución**: Verificar que se esté usando el tenant correcto de RUITOQUE E.S.P

### Error: "Insufficient privileges"
**Causa**: Faltan permisos de API
**Solución**: Agregar todos los permisos listados en el Paso 2

### Error: "Invalid client secret"
**Causa**: El secret de cliente es incorrecto o expiró
**Solución**: Crear un nuevo secret de cliente

### Error: "Consent required"
**Causa**: No se ha concedido consentimiento de administrador
**Solución**: Ejecutar "Conceder consentimiento de administrador"

## 🔄 Solución Temporal

Mientras se configura Azure AD correctamente, la aplicación puede funcionar con autenticación básica:

1. **Verificar credenciales** en `config/constants.py`
2. **Verificar permisos** del usuario en SharePoint
3. **Contactar al administrador** de SharePoint si es necesario

## 📞 Soporte

Para problemas con la configuración de Azure AD:
- **Administrador de Azure**: [correo del administrador]
- **Equipo de Desarrollo**: [correo del equipo]
- **Documentación Microsoft**: [docs.microsoft.com](https://docs.microsoft.com)

---

**Nota**: Esta configuración es necesaria para usar Azure AD. Si no se puede configurar, la aplicación funcionará con autenticación básica pero puede tener limitaciones de seguridad.
