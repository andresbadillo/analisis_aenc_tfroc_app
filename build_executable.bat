@echo off
REM Script para crear el ejecutable de la aplicación Streamlit
REM Este script crea un ejecutable .exe que puede ejecutarse sin necesidad de Python instalado

echo ========================================
echo Creando ejecutable de la aplicacion
echo ========================================
echo.

REM Verificar que Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    pause
    exit /b 1
)

REM Verificar que PyInstaller esta instalado
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo PyInstaller no esta instalado. Instalando...
    pip install pyinstaller
)

REM Verificar si el ejecutable anterior esta en ejecucion
echo Verificando si hay procesos en ejecucion...
tasklist /FI "IMAGENAME eq AnalisisAENC_TFROC.exe" 2>NUL | find /I /N "AnalisisAENC_TFROC.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ADVERTENCIA: El ejecutable esta en ejecucion. Cerrandolo...
    taskkill /F /IM AnalisisAENC_TFROC.exe >NUL 2>&1
    timeout /t 2 /nobreak >NUL
)

REM Limpiar builds anteriores con reintentos
echo Limpiando builds anteriores...
if exist build (
    echo Eliminando directorio build...
    timeout /t 1 /nobreak >NUL
    rmdir /s /q build 2>NUL
    if exist build (
        echo Advertencia: No se pudo eliminar build completamente. Continuando...
    )
)
if exist dist (
    echo Eliminando directorio dist...
    timeout /t 1 /nobreak >NUL
    rmdir /s /q dist 2>NUL
    if exist dist (
        echo Advertencia: No se pudo eliminar dist completamente. Continuando...
    )
)
if exist __pycache__ (
    rmdir /s /q __pycache__ 2>NUL
)

REM Crear el ejecutable
echo.
echo Creando ejecutable...
echo Esto puede tardar varios minutos...
echo.

pyinstaller build_executable.spec --clean

if errorlevel 1 (
    echo.
    echo ERROR: No se pudo crear el ejecutable
    pause
    exit /b 1
)

echo.
echo ========================================
echo Ejecutable creado exitosamente!
echo ========================================
echo.
echo El ejecutable se encuentra en: dist\AnalisisAENC_TFROC.exe
echo.
echo Puedes copiar este archivo a cualquier ubicacion y ejecutarlo directamente.
echo.
echo IMPORTANTE: Asegurate de tener el archivo .env con las credenciales
echo en el mismo directorio que el ejecutable, o en la ubicacion especificada
echo en la configuracion de la aplicacion.
echo.
pause

