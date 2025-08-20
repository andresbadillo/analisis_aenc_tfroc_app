# 🔐 Guía de Permisos de Azure AD

## 🚨 Problema Identificado
El sitio de SharePoint existe y puedes acceder manualmente, pero la aplicación no puede conectarse. Esto indica un problema de permisos en Azure AD.

## 🔍 Verificación de Permisos

### Paso 1: Ir a Azure Portal
1. Ve a: https://portal.azure.com
2. Inicia sesión con tu cuenta de RUITOQUE

### Paso 2: Encontrar tu aplicación
1. Ve a **Azure Active Directory**
2. Selecciona **Registros de aplicaciones**
3. Busca tu aplicación: **"Análisis AENC TFROC - RUITOQUE"**
4. Haz clic en la aplicación

### Paso 3: Verificar permisos de API
1. En el menú izquierdo, selecciona **Permisos de API**
2. Verifica que tienes estos permisos de **Microsoft Graph**:

#### Permisos Requeridos:
- ✅ **Sites.Read.All** - Leer información de sitios
- ✅ **Sites.ReadWrite.All** - Leer y escribir en sitios
- ✅ **Files.Read.All** - Leer archivos
- ✅ **Files.ReadWrite.All** - Leer y escribir archivos

### Paso 4: Verificar consentimiento
1. En la sección de permisos, verifica que aparece:
   - **Estado:** Consentimiento concedido
   - **Concedido por:** [Tu nombre o administrador]

2. Si no aparece "Consentimiento concedido":
   - Haz clic en **Conceder consentimiento de administrador**
   - Confirma la acción

## 🛠️ Configuración de Permisos

### Si faltan permisos:

1. **Agregar permisos faltantes:**
   - Haz clic en **Agregar un permiso**
   - Selecciona **Microsoft Graph**
   - Selecciona **Permisos de aplicación**
   - Busca y agrega los permisos faltantes

2. **Conceder consentimiento:**
   - Después de agregar permisos, haz clic en **Conceder consentimiento de administrador**
   - Confirma la acción

### Permisos específicos a agregar:

```
Microsoft Graph > Permisos de aplicación:
- Sites.Read.All
- Sites.ReadWrite.All
- Files.Read.All
- Files.ReadWrite.All
```

## 🔧 Verificación Adicional

### Verificar configuración de la aplicación:
1. En **Información general**, verifica:
   - **ID de aplicación (cliente):** Debe coincidir con AZURE_CLIENT_ID en .env
   - **ID de directorio (inquilino):** Debe coincidir con AZURE_TENANT_ID en .env

### Verificar secretos:
1. Ve a **Certificados y secretos**
2. Verifica que tienes un secreto válido
3. Copia el valor del secreto a AZURE_CLIENT_SECRET en .env

## 🚨 Problemas Comunes

### Error 403 - Forbidden
**Causa:** La aplicación no tiene permisos suficientes
**Solución:** Agregar los permisos requeridos y conceder consentimiento

### Error 401 - Unauthorized
**Causa:** Token inválido o expirado
**Solución:** Verificar credenciales en .env y regenerar token

### Error 404 - Not Found
**Causa:** Sitio no encontrado (ya descartado en tu caso)
**Solución:** Verificar nombre del sitio

## 📋 Checklist de Verificación

- [ ] La aplicación está registrada en Azure AD
- [ ] Los permisos de Microsoft Graph están configurados
- [ ] El consentimiento de administrador fue concedido
- [ ] Las credenciales en .env son correctas
- [ ] El token se genera correctamente

## 🎯 Próximos Pasos

1. **Verifica los permisos** siguiendo esta guía
2. **Ejecuta el script de diagnóstico** para confirmar
3. **Prueba la aplicación** nuevamente
4. **Si persiste el problema**, contacta al administrador de Azure AD

## 📞 Contacto de Soporte

Si necesitas ayuda con la configuración de Azure AD:
- Contacta al administrador de Azure AD de RUITOQUE
- Proporciona el ID de la aplicación y los permisos requeridos
- Solicita que concedan el consentimiento de administrador

---

**Nota:** Esta guía asume que tienes acceso de administrador a Azure AD. Si no lo tienes, contacta al administrador correspondiente.
