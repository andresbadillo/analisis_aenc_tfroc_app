# Guía para Crear Ejecutable de la Aplicación

Esta guía explica cómo crear un ejecutable de escritorio (.exe) para la aplicación de análisis AENC y TFROC, que se ejecutará automáticamente en el navegador en `http://localhost:8501`.

## 📋 Requisitos Previos

1. **Python 3.8+** instalado en tu sistema
2. Todas las dependencias instaladas (ejecutar `pip install -r requirements.txt`)
3. **PyInstaller** (se instalará automáticamente si no está presente)

## 🚀 Creación del Ejecutable

### Método 1: Usar el Script Automático (Recomendado)

1. Abre una terminal en el directorio del proyecto
2. Ejecuta el script de construcción:

**Windows:**
```bash
build_executable.bat
```

**Linux/Mac:**
```bash
chmod +x build_executable.sh
./build_executable.sh
```

### Método 2: Usar PyInstaller Directamente

1. Asegúrate de tener PyInstaller instalado:
```bash
pip install pyinstaller
```

2. Ejecuta PyInstaller con el archivo spec:
```bash
pyinstaller build_executable.spec --clean
```

## 📦 Resultado

Después de la compilación, encontrarás el ejecutable en:
```
dist/AnalisisAENC_TFROC.exe
```

## 🎯 Uso del Ejecutable

1. **Copiar el ejecutable**: Puedes copiar `AnalisisAENC_TFROC.exe` a cualquier ubicación
2. **Archivo .env**: Asegúrate de tener el archivo `.env` con las credenciales de Azure AD en el mismo directorio que el ejecutable
3. **Ejecutar**: Doble clic en el ejecutable
4. **Navegador**: El navegador se abrirá automáticamente en `http://localhost:8501`

## ⚙️ Configuración del Ejecutable

### Cambiar el Nombre del Ejecutable

Edita `build_executable.spec` y cambia la línea:
```python
name='AnalisisAENC_TFROC',
```

### Agregar un Icono

1. Prepara un archivo `.ico` (Windows) o `.icns` (Mac)
2. Edita `build_executable.spec` y cambia:
```python
icon='ruta/a/tu/icono.ico'
```

### Ocultar la Consola

Si quieres ocultar la ventana de consola (solo Windows), cambia en `build_executable.spec`:
```python
console=False,  # Cambiar de True a False
```

**Nota**: Si ocultas la consola, no podrás ver los logs de la aplicación.

## 📁 Estructura de Archivos Necesarios

El ejecutable incluye automáticamente:
- ✅ Todos los módulos Python (`config/`, `utils/`, `auth/`)
- ✅ Archivos de assets (`assets/`)
- ✅ Archivos de configuración (`streamlit.toml`)
- ✅ Todas las dependencias necesarias

**Importante**: El archivo `.env` NO se incluye en el ejecutable por seguridad. Debes copiarlo manualmente junto con el ejecutable.

## 🔧 Solución de Problemas

### Error: "No se encontró el archivo app.py"

- Asegúrate de que `app.py` esté en el mismo directorio que el ejecutable
- O ejecuta el ejecutable desde el directorio del proyecto

### Error: "Módulo no encontrado"

- Verifica que todas las dependencias estén en `requirements.txt`
- Agrega el módulo faltante a `hiddenimports` en `build_executable.spec`
- Recompila el ejecutable

### Error: "No se puede abrir el navegador"

- Verifica que el puerto 8501 no esté en uso
- Asegúrate de tener permisos de firewall para la aplicación
- Abre manualmente `http://localhost:8501` en tu navegador

### El ejecutable es muy grande

- Es normal: PyInstaller incluye Python y todas las dependencias
- Tamaño típico: 100-300 MB
- Puedes usar UPX para comprimir (ya está habilitado en el spec)

### El ejecutable no funciona en otra computadora

- Verifica que el archivo `.env` esté presente
- Algunos antivirus pueden bloquear ejecutables creados con PyInstaller
- Asegúrate de que la computadora destino tenga permisos de ejecución

## 📝 Notas Importantes

1. **Seguridad**: El archivo `.env` contiene credenciales sensibles. No lo incluyas en el ejecutable.

2. **Actualizaciones**: Si actualizas el código, necesitas recompilar el ejecutable.

3. **Dependencias**: El ejecutable incluye todas las dependencias, por lo que no necesitas Python instalado en la computadora destino.

4. **Puerto**: El ejecutable usa el puerto 8501 por defecto. Si está ocupado, Streamlit intentará usar otro puerto.

5. **Logs**: Los logs de Streamlit se muestran en la consola del ejecutable.

## 🆘 Soporte

Si encuentras problemas:
1. Revisa los mensajes de error en la consola
2. Verifica que todos los archivos necesarios estén presentes
3. Consulta la documentación de PyInstaller: https://pyinstaller.org/

