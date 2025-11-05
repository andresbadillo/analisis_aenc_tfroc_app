#!/bin/bash

# Script para crear el ejecutable de la aplicación Streamlit
# Este script crea un ejecutable que puede ejecutarse sin necesidad de Python instalado

echo "========================================"
echo "Creando ejecutable de la aplicación"
echo "========================================"
echo ""

# Verificar que Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado o no está en el PATH"
    exit 1
fi

# Verificar que PyInstaller está instalado
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "PyInstaller no está instalado. Instalando..."
    pip3 install pyinstaller
fi

# Limpiar builds anteriores
echo "Limpiando builds anteriores..."
rm -rf build dist __pycache__

# Crear el ejecutable
echo ""
echo "Creando ejecutable..."
echo "Esto puede tardar varios minutos..."
echo ""

pyinstaller build_executable.spec --clean

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: No se pudo crear el ejecutable"
    exit 1
fi

echo ""
echo "========================================"
echo "Ejecutable creado exitosamente!"
echo "========================================"
echo ""
echo "El ejecutable se encuentra en: dist/AnalisisAENC_TFROC"
echo ""
echo "Puedes copiar este archivo a cualquier ubicación y ejecutarlo directamente."
echo ""
echo "IMPORTANTE: Asegúrate de tener el archivo .env con las credenciales"
echo "en el mismo directorio que el ejecutable, o en la ubicación especificada"
echo "en la configuración de la aplicación."
echo ""

