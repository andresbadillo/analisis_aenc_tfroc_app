@echo off
REM Script para limpiar directorios de build bloqueados
REM Úsalo si tienes problemas de permisos al compilar

echo ========================================
echo Limpiando directorios de build
echo ========================================
echo.

REM Cerrar el ejecutable si esta en ejecucion
echo Verificando procesos en ejecucion...
tasklist /FI "IMAGENAME eq AnalisisAENC_TFROC.exe" 2>NUL | find /I /N "AnalisisAENC_TFROC.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Cerrando AnalisisAENC_TFROC.exe...
    taskkill /F /IM AnalisisAENC_TFROC.exe
    timeout /t 2 /nobreak
)

REM Cerrar procesos de Python que puedan estar usando archivos
echo Cerrando procesos de Python relacionados...
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| find "PID:"') do (
    taskkill /F /PID %%a >NUL 2>&1
)

timeout /t 2 /nobreak

REM Intentar eliminar directorios
echo.
echo Eliminando directorios...

if exist build (
    echo - Eliminando build...
    rmdir /s /q build
    if exist build (
        echo   ERROR: No se pudo eliminar build. Cierra todas las ventanas y procesos relacionados.
    ) else (
        echo   OK: build eliminado
    )
)

if exist dist (
    echo - Eliminando dist...
    rmdir /s /q dist
    if exist dist (
        echo   ERROR: No se pudo eliminar dist. Cierra todas las ventanas y procesos relacionados.
    ) else (
        echo   OK: dist eliminado
    )
)

if exist __pycache__ (
    echo - Eliminando __pycache__...
    for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
)

echo.
echo Limpieza completada.
echo.
pause

