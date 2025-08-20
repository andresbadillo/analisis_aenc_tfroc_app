# 🔧 Solución de Problemas: Conexión a SharePoint

## 🚨 Problema Actual
La aplicación puede autenticarse con Azure AD, pero no se conecta a SharePoint.

## 🔍 Diagnóstico Inmediato

### 1. Verificar que el sitio existe
**Paso crítico:** Ve directamente a SharePoint y verifica que el sitio existe:
- **URL:** https://ruitoqueesp1.sharepoint.com/sites/fronterascomerciales
- **Acción:** Confirma que puedes acceder al sitio
- **Resultado esperado:** Deberías ver el sitio de SharePoint

### 2. Verificar permisos de la aplicación
Tu aplicación de Azure AD necesita estos permisos **EXACTOS**:

#### Permisos de Microsoft Graph API:
- ✅ `Sites.Read.All`
- ✅ `Sites.ReadWrite.All`
- ✅ `Files.Read.All`
- ✅ `Files.ReadWrite.All`

#### Cómo verificar en Azure Portal:
1. Ve a: https://portal.azure.com
2. Azure Active Directory > Registros de aplicaciones
3. Selecciona tu aplicación "Análisis AENC TFROC - RUITOQUE"
4. Permisos de API > Microsoft Graph
5. **Verifica que todos los permisos estén concedidos**

### 3. Verificar consentimiento de administrador
- Los permisos deben mostrar "Consentimiento concedido" por un administrador
- Si no están concedidos, contacta al administrador de Azure AD

## 🛠️ Soluciones Específicas

### Solución 1: Verificar nombre del sitio
El nombre del sitio puede ser diferente. Prueba estas variaciones:

```python
# En config/constants.py, prueba estos nombres:
SHAREPOINT_CONFIG = {
    'url': 'https://ruitoqueesp1.sharepoint.com',
    'site': 'fronterascomerciales',  # Original
    # 'site': 'FronterasComerciales',  # Con mayúsculas
    # 'site': 'fronteras-comerciales',  # Con guiones
    # 'site': 'fronteras_comerciales',  # Con guiones bajos
}
```

### Solución 2: Usar ID del sitio
Si el nombre no funciona, usa el ID del sitio:

1. Ve a SharePoint y obtén el ID del sitio
2. Actualiza la configuración:

```python
SHAREPOINT_CONFIG = {
    'url': 'https://ruitoqueesp1.sharepoint.com',
    'site_id': 'tu_site_id_aqui',  # Usar ID en lugar de nombre
}
```

### Solución 3: Probar con sitio raíz
Para verificar que la configuración funciona:

```python
SHAREPOINT_CONFIG = {
    'url': 'https://ruitoqueesp1.sharepoint.com',
    'site': 'sites',  # Sitio raíz (siempre existe)
}
```

## 🔧 Scripts de Diagnóstico

### Ejecutar diagnóstico detallado:
```bash
streamlit run test_sharepoint_detailed.py
```

### Verificar configuración:
```bash
streamlit run test_sharepoint_connection.py
```

## 📞 Pasos de Emergencia

### Si nada funciona:

1. **Contactar al administrador de SharePoint** para verificar:
   - Que el sitio `fronterascomerciales` existe
   - Que tu cuenta tiene acceso
   - Que la aplicación de Azure AD tiene permisos

2. **Verificar en Azure Portal**:
   - Que la aplicación está registrada correctamente
   - Que los permisos están configurados
   - Que el consentimiento fue concedido

3. **Probar con credenciales básicas** (temporalmente):
   - Revertir a la configuración anterior con usuario/contraseña
   - Solo para verificar que el problema es específico de Azure AD

## 📋 Checklist de Verificación

- [ ] El sitio `fronterascomerciales` existe en SharePoint
- [ ] Puedes acceder al sitio con tu cuenta
- [ ] La aplicación de Azure AD tiene los permisos correctos
- [ ] El consentimiento de administrador fue concedido
- [ ] El token de Azure AD es válido
- [ ] La configuración en `constants.py` es correcta

## 🎯 Próximos Pasos

1. **Inmediato:** Ve a SharePoint y verifica que el sitio existe
2. **Verificar permisos:** Confirma los permisos de la aplicación en Azure AD
3. **Probar nombres:** Intenta diferentes variaciones del nombre del sitio
4. **Contactar administrador:** Si nada funciona, contacta al administrador

## 🚨 Información Crítica

**El problema más común es que el sitio no existe o tiene un nombre diferente.**

**Verifica manualmente en SharePoint antes de continuar con la configuración técnica.**

---

**Nota**: Este documento se actualiza según los problemas encontrados.
