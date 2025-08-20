# Manual de Usuario - Análisis AENC y TFROC

## 📖 Introducción

Este manual describe cómo usar la aplicación de Análisis AENC y TFROC desarrollada para RUITOQUE E.S.P. La aplicación automatiza el proceso de descarga, procesamiento y carga de archivos de energía desde el servidor FTP de XM hacia SharePoint.

## 🎯 Objetivo

La aplicación tiene como objetivo principal:
- Descargar archivos AENC y TFROC desde el servidor FTP de XM
- Procesar y transformar los datos según las reglas de negocio
- Cargar los archivos procesados en SharePoint
- Actualizar el archivo de consumo anual consolidado

## 🚀 Inicio Rápido

### 1. Acceder a la aplicación
- Abrir el navegador web
- Navegar a la URL de la aplicación
- La interfaz se cargará automáticamente

### 2. Verificar el estado
- Revisar el panel lateral derecho para ver el estado de las conexiones
- Verificar que no haya errores de conexión
- Comprobar que la configuración de Azure AD esté completa

### 3. Ejecutar los pasos
- Seguir los 4 pasos en orden secuencial
- Cada paso debe completarse antes de continuar con el siguiente

## 📋 Pasos Detallados

### Paso 1: Descargar archivos desde FTP

**¿Qué hace?**
- Verifica si ya existen archivos .TxF en SharePoint
- Si no existen, conecta al servidor FTP de XM
- Descarga archivos AENC y TFROC del mes actual y anterior
- Prioriza versiones de archivos (.TxF > .TxR > .Tx2)

**Lógica del proceso:**
1. **Verificación**: Revisa si ya existen archivos en SharePoint
2. **Decisión**: 
   - Si existen archivos → No descarga del FTP
   - Si no existen archivos → Procede con la descarga del FTP
3. **Descarga**: Conecta al FTP y descarga archivos necesarios

**Cómo ejecutar:**
1. Hacer clic en "🚀 Ejecutar Paso 1: Descargar archivos"
2. Esperar a que se complete la verificación y descarga
3. Verificar que aparezca el mensaje de éxito

**Indicadores de éxito:**
- ✅ Mensaje: "Conexión SharePoint establecida"
- ✅ Mensaje: "Paso 1 completado: X archivos descargados" (si es necesario)
- ✅ Mensaje: "Paso 1 completado: Archivos ya existen en SharePoint" (si ya existen)
- Estado FTP: Conectado (verde en el sidebar)

**Posibles errores:**
- ❌ "No se pudo conectar a SharePoint"
- ❌ "No se pudo conectar al servidor FTP"
- ❌ "No se pudieron descargar archivos"

**Solución de problemas:**
- Verificar conectividad de red
- Comprobar credenciales de SharePoint y FTP
- Contactar al administrador si persiste el error

### Paso 2: Subir archivos a SharePoint

**¿Qué hace?**
- Conecta a SharePoint
- Verifica si ya existen archivos .TxF
- Sube archivos descargados
- Limpia archivos según prioridad

**Cómo ejecutar:**
1. Asegurarse de que el Paso 1 esté completado
2. Hacer clic en "🚀 Ejecutar Paso 2: Subir archivos"
3. Esperar a que se complete la subida

**Indicadores de éxito:**
- ✅ Mensaje: "Paso 2 completado: Archivos subidos exitosamente"
- Estado SharePoint: Conectado (verde en el sidebar)

**Posibles errores:**
- ❌ "No se pudo conectar a SharePoint"
- ❌ "Error al subir algunos archivos"

**Solución de problemas:**
- Verificar credenciales de SharePoint
- Comprobar permisos de acceso
- Contactar al administrador si persiste el error

### Paso 3: Procesar datos AENC y TFROC

**¿Qué hace?**
- Carga archivos desde SharePoint
- Procesa datos día a día
- Aplica transformaciones y cálculos
- Genera archivos CSV consolidados

**Archivos generados:**
- `aenc_consolidado_{mes}_{año}.csv`
- `consumos_{mes}_{año}.csv`
- `total_consumo_{mes}_{año}.csv`

**Cómo ejecutar:**
1. Asegurarse de que el Paso 2 esté completado
2. Hacer clic en "🚀 Ejecutar Paso 3: Procesar datos"
3. Esperar a que se complete el procesamiento

**Indicadores de éxito:**
- ✅ Mensaje: "Paso 3 completado: Datos procesados exitosamente"
- Estado: Archivos procesados (verde en el sidebar)

**Posibles errores:**
- ❌ "No se pudo conectar a SharePoint"
- ❌ "Error al procesar algunos datos"

**Solución de problemas:**
- Verificar que los archivos tengan el formato correcto
- Comprobar que existan archivos AENC y TFROC correspondientes
- Contactar al administrador si persiste el error

### Paso 4: Actualizar archivo de consumo anual

**¿Qué hace?**
- Carga archivo de consumo anual desde SharePoint
- Actualiza con datos del mes procesado
- Sube archivo actualizado

**Ubicación del archivo:**
- `Documentos Compartidos/aenc/fact_consumos/consumos_{año}.csv`

**Cómo ejecutar:**
1. Asegurarse de que el Paso 3 esté completado
2. Hacer clic en "🚀 Ejecutar Paso 4: Actualizar consumo anual"
3. Esperar a que se complete la actualización

**Indicadores de éxito:**
- ✅ Mensaje: "Paso 4 completado: Archivo anual actualizado exitosamente"

**Posibles errores:**
- ❌ "No se pudo conectar a SharePoint"
- ❌ "Error al actualizar archivo anual"

**Solución de problemas:**
- Verificar permisos de escritura en SharePoint
- Comprobar que exista el archivo anual
- Contactar al administrador si persiste el error

## 🎉 Proceso Completado

Cuando todos los pasos se han ejecutado exitosamente, aparecerá una sección de resumen que confirma:

✅ **¡Todos los pasos han sido completados exitosamente!**

**Resumen de lo realizado:**
- ✅ Archivos descargados desde FTP
- ✅ Archivos subidos a SharePoint
- ✅ Datos procesados y consolidados
- ✅ Archivo de consumo anual actualizado

## 🔧 Acciones Adicionales

### Limpiar archivos temporales
- **Ubicación**: Panel lateral → Acciones → "🗑️ Limpiar archivos temporales"
- **Propósito**: Eliminar archivos descargados del servidor local
- **Cuándo usar**: Después de completar todo el proceso

### Reiniciar aplicación
- **Ubicación**: Panel lateral → Acciones → "🔄 Reiniciar aplicación"
- **Propósito**: Limpiar el estado de la sesión y comenzar de nuevo
- **Cuándo usar**: Si hay errores persistentes o se quiere empezar de nuevo

## 📊 Monitoreo del Estado

### Panel lateral - Estado actual
- **FTP**: Indica si la conexión FTP está activa
- **SharePoint**: Indica si la conexión SharePoint está activa
- **Archivos descargados**: Indica si se han descargado archivos
- **Archivos procesados**: Indica si se han procesado archivos
- **Configuración Azure AD**: Indica si la configuración de Azure AD está completa

### Configuración de Azure AD
La aplicación requiere configuración de Azure Active Directory para funcionar correctamente:

1. **Crear archivo .env**: En la raíz del proyecto, crear un archivo llamado `.env`
2. **Configurar variables**: Agregar las siguientes variables al archivo `.env`:
   ```
   AZURE_TENANT_ID=tu_tenant_id
   AZURE_CLIENT_ID=tu_client_id
   AZURE_CLIENT_SECRET=tu_client_secret
   AZURE_REDIRECT_URI=http://localhost:8501
   ```
3. **Verificar estado**: En el panel lateral, verificar que aparezca "✅ Configuración Azure AD completa"

### Mensajes de estado
- **Éxito**: Mensajes en verde con ✅
- **Error**: Mensajes en rojo con ❌
- **Advertencia**: Mensajes en amarillo con ⚠️
- **Información**: Mensajes en azul con ℹ️

## 🚨 Solución de Problemas Comunes

### Error de conexión FTP
**Síntomas:**
- Mensaje: "No se pudo conectar al servidor FTP"
- Estado FTP en rojo

**Soluciones:**
1. Verificar conectividad de red
2. Comprobar que el servidor FTP esté disponible
3. Contactar al administrador para verificar credenciales

### Error de conexión SharePoint
**Síntomas:**
- Mensaje: "No se pudo conectar a SharePoint"
- Estado SharePoint en rojo

**Soluciones:**
1. Verificar credenciales de SharePoint
2. Comprobar permisos de acceso
3. Verificar que la URL de SharePoint sea correcta

### Error de procesamiento de datos
**Síntomas:**
- Mensaje: "Error al procesar algunos datos"
- Paso 3 no se completa

**Soluciones:**
1. Verificar que los archivos tengan el formato esperado
2. Comprobar que existan archivos AENC y TFROC correspondientes
3. Verificar permisos de escritura en carpeta temporal

### Archivos ya existen en SharePoint
**Síntomas:**
- Mensaje: "📁 Archivos .TxF ya existen en SharePoint para {año}-{mes}"
- Mensaje: "⚠️ Los archivos ya existen en SharePoint para ambos meses"
- Mensaje: "Paso 1 completado: Archivos ya existen en SharePoint"

**Explicación:**
- Esto es normal y no es un error
- La aplicación verifica primero si ya existen archivos antes de descargar del FTP
- Si los archivos ya existen, no se descargan del FTP para evitar duplicados
- Se puede continuar con el siguiente paso

### No se encontraron archivos en SharePoint
**Síntomas:**
- Mensaje: "📁 No se encontraron archivos .TxF en SharePoint para {año}-{mes}"
- Mensaje: "✅ Procediendo con la descarga del FTP..."

**Explicación:**
- Esto es normal cuando los archivos no existen en SharePoint
- La aplicación procederá automáticamente a descargar los archivos del FTP
- No requiere acción adicional del usuario

### Error de configuración Azure AD
**Síntomas:**
- Mensaje: "❌ Configuración Azure AD incompleta"
- Estado Azure AD en rojo en el panel lateral

**Soluciones:**
1. Verificar que existe el archivo `.env` en la raíz del proyecto
2. Comprobar que todas las variables de Azure AD están configuradas:
   - AZURE_TENANT_ID
   - AZURE_CLIENT_ID
   - AZURE_CLIENT_SECRET
   - AZURE_REDIRECT_URI
3. Verificar que la aplicación esté registrada en Azure Portal
4. Comprobar que los permisos de API estén configurados
5. Contactar al administrador si persiste el error

## 📞 Soporte Técnico

### Contacto
Para soporte técnico o preguntas sobre la aplicación:
- **Equipo**: Desarrollo RUITOQUE E.S.P
- **Email**: [correo de soporte]
- **Teléfono**: [número de soporte]

### Información para reportar problemas
Al reportar un problema, incluir:
1. **Descripción del error**: Qué paso falló
2. **Mensaje de error**: Texto exacto del mensaje
3. **Pasos para reproducir**: Qué acciones llevaron al error
4. **Fecha y hora**: Cuándo ocurrió el error
5. **Estado de las conexiones**: Qué indicadores estaban en verde/rojo

## 📝 Notas Importantes

### Frecuencia de uso
- La aplicación está diseñada para ejecutarse **una vez por mes**
- Se procesan automáticamente el **mes actual y el mes anterior**
- No es necesario ejecutar múltiples veces en el mismo día

### Archivos generados
- Los archivos se guardan en SharePoint con nombres específicos
- No se sobrescriben archivos existentes
- Se mantiene un historial completo de archivos procesados

### Seguridad
- Las credenciales están configuradas en el servidor
- No se almacenan datos sensibles en el navegador
- Las conexiones se cierran automáticamente después de cada paso

---

**Versión del manual**: 1.0  
**Última actualización**: 2025  
**Aplicación**: Análisis AENC y TFROC - RUITOQUE E.S.P
