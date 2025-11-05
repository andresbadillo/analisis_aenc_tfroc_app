# 📦 Instrucciones Simples para Crear y Usar el Ejecutable

## 🎯 Usar el Ejecutable (Ya Creado)

El ejecutable ya está listo en la carpeta `dist`. Para usarlo:

1. **Abre el Explorador de Archivos** de Windows
2. **Ve a la carpeta `dist`** del proyecto
3. **Haz doble clic** en `AnalisisAENC_TFROC.exe`
4. **Espera** unos segundos - el navegador se abrirá automáticamente
5. **¡Listo!** La aplicación estará funcionando

**⚠️ IMPORTANTE:** 
- Copia tu archivo `.env` (con las credenciales de Azure) a la carpeta `dist`, junto al ejecutable
- Si no tienes el `.env`, la aplicación no podrá conectarse a SharePoint

---

## 🔨 Crear el Ejecutable de Nuevo (Si Hiciste Cambios)

Si modificaste el código y necesitas crear un nuevo ejecutable:

### Opción 1: Usar el Script Automático (Más Fácil)

1. **Abre PowerShell** (o CMD):
   - Presiona `Windows + R`
   - Escribe `powershell` y presiona Enter
   - O busca "PowerShell" en el menú de inicio

2. **Navega al directorio del proyecto:**
   ```powershell
   cd "C:\Users\rbadillo\OneDrive - RUITOQUE E.S.P\Documentos 1\Proyectos_Dev\analisis_aenc_tfroc_app"
   ```

3. **Ejecuta el script:**
   ```powershell
   .\build_executable.bat
   ```

4. **Espera** (puede tardar 5-10 minutos)
5. Cuando termine, el ejecutable estará en la carpeta `dist`

### Opción 2: Paso a Paso Manual

Si el script automático no funciona:

1. **Cierra** cualquier ventana de la aplicación o PowerShell abierta

2. **Abre PowerShell** y navega al proyecto:
   ```powershell
   cd "C:\Users\rbadillo\OneDrive - RUITOQUE E.S.P\Documentos 1\Proyectos_Dev\analisis_aenc_tfroc_app"
   ```

3. **Ejecuta el comando:**
   ```powershell
   pyinstaller build_executable.spec --clean
   ```

4. **Espera** a que termine (puede tardar varios minutos)

---

## 🐛 Solución de Problemas

### Error: "No se puede eliminar el directorio build"

**Solución:**
1. Cierra todas las ventanas de PowerShell/CMD
2. Cierra el ejecutable si está abierto
3. Ejecuta el script de limpieza:
   ```powershell
   .\clean_build.bat
   ```
4. Luego ejecuta el build de nuevo

### Error: "No se encontró app.py"

**Solución:**
- Asegúrate de estar en el directorio correcto del proyecto
- Verifica que el archivo `app.py` exista en el directorio

### Error: "PyInstaller no está instalado"

**Solución:**
```powershell
pip install pyinstaller
```

---

## 📝 Notas Importantes

- **El ejecutable es grande** (100-300 MB) porque incluye Python y todas las dependencias
- **No necesitas Python instalado** para ejecutar el `.exe` en otra computadora
- **El archivo `.env` NO se incluye** por seguridad - debes copiarlo manualmente
- **Si cambias el código**, necesitas recompilar el ejecutable

---

## ✅ Checklist Antes de Usar el Ejecutable

- [ ] El ejecutable `AnalisisAENC_TFROC.exe` está en la carpeta `dist`
- [ ] El archivo `.env` está copiado en la carpeta `dist` (junto al ejecutable)
- [ ] La carpeta `assets` no es necesaria (se incluye en el ejecutable)
- [ ] Puedes ejecutar el `.exe` desde cualquier ubicación (después de copiar el `.env`)

---

## 🆘 ¿Necesitas Ayuda?

Si tienes problemas:
1. Revisa los mensajes de error en la consola
2. Verifica que todos los archivos necesarios estén presentes
3. Asegúrate de que no haya procesos bloqueando archivos

