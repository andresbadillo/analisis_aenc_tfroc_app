"""
Script launcher para ejecutar la aplicación Streamlit como ejecutable de escritorio.
Este script inicia el servidor Streamlit y abre automáticamente el navegador.
"""

import subprocess
import sys
import os
import time
from pathlib import Path

# Configurar codificación UTF-8 para la consola de Windows
if sys.platform == 'win32':
    try:
        # Intentar configurar UTF-8 en la consola
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def get_app_path():
    """Obtiene la ruta base de la aplicación."""
    if getattr(sys, 'frozen', False):
        # Si estamos ejecutando desde un ejecutable
        # PyInstaller crea un directorio temporal y almacena la ruta en _MEIPASS
        if hasattr(sys, '_MEIPASS'):
            # Los archivos de datos se extraen aquí
            return Path(sys._MEIPASS)
        else:
            # Fallback: directorio del ejecutable
            return Path(sys.executable).parent
    else:
        # Si estamos ejecutando desde el script
        return Path(__file__).parent

def wait_for_server(url="http://localhost:8501", timeout=30):
    """Espera a que el servidor Streamlit esté listo."""
    import urllib.request
    import urllib.error
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = urllib.request.urlopen(url, timeout=1)
            if response.status == 200:
                return True
        except (urllib.error.URLError, OSError):
            pass
        time.sleep(0.5)
    return False

def safe_print(text):
    """Imprime texto de forma segura, manejando errores de codificación."""
    try:
        print(text)
    except UnicodeEncodeError:
        # Si falla, reemplazar caracteres problemáticos
        safe_text = text.encode('ascii', 'replace').decode('ascii')
        print(safe_text)

def main():
    """Función principal que ejecuta Streamlit."""
    # Información de debugging al inicio
    print("=" * 60)
    safe_print("Informacion de Depuracion")
    print("=" * 60)
    print(f"Ejecutando desde ejecutable: {getattr(sys, 'frozen', False)}")
    if getattr(sys, 'frozen', False):
        print(f"Ruta del ejecutable: {sys.executable}")
        print(f"Directorio del ejecutable: {Path(sys.executable).parent}")
        if hasattr(sys, '_MEIPASS'):
            print(f"Directorio temporal (_MEIPASS): {sys._MEIPASS}")
            meipass_path = Path(sys._MEIPASS)
            if meipass_path.exists():
                print(f"\nArchivos en _MEIPASS ({meipass_path}):")
                try:
                    for item in sorted(meipass_path.iterdir()):
                        tipo = "[DIR]" if item.is_dir() else "[FILE]"
                        print(f"  {tipo} {item.name}")
                except Exception as e:
                    print(f"  Error al listar: {e}")
        else:
            print("ADVERTENCIA: _MEIPASS no esta disponible")
            print(f"\nArchivos en directorio del ejecutable:")
            try:
                exe_dir = Path(sys.executable).parent
                for item in sorted(exe_dir.iterdir()):
                    tipo = "[DIR]" if item.is_dir() else "[FILE]"
                    print(f"  {tipo} {item.name}")
            except Exception as e:
                print(f"  Error al listar: {e}")
    print("=" * 60)
    print()
    
    app_path = get_app_path()
    app_file = app_path / "app.py"
    
    print(f"Buscando app.py en: {app_path}")
    print(f"Ruta completa: {app_file}")
    print(f"¿Existe?: {app_file.exists()}")
    print()
    
    # Verificar que el archivo app.py existe
    if not app_file.exists():
        print(f"ERROR: No se encontro el archivo app.py en {app_path}")
        print(f"\nIntentando buscar app.py en otras ubicaciones...")
        
        # Intentar buscar en diferentes ubicaciones
        search_paths = []
        if getattr(sys, 'frozen', False):
            if hasattr(sys, '_MEIPASS'):
                search_paths.append(Path(sys._MEIPASS))
            search_paths.append(Path(sys.executable).parent)
        else:
            search_paths.append(Path(__file__).parent)
        
        for search_path in search_paths:
            test_file = search_path / "app.py"
            exists_text = "Existe" if test_file.exists() else "No existe"
            print(f"  Probando: {test_file} - {exists_text}")
            if test_file.exists():
                print(f"\n¡Encontrado! Usando: {test_file}")
                app_path = search_path
                app_file = test_file
                break
        
        if not app_file.exists():
            print("\nERROR: No se pudo encontrar app.py en ninguna ubicacion")
            input("Presiona Enter para salir...")
            sys.exit(1)
    
    # Cambiar al directorio de la aplicación (donde están los assets)
    # Esto es importante para que los assets se encuentren correctamente
    os.chdir(app_path)
    
    # Configurar el path del archivo .env
    # El .env debe estar en el mismo directorio que el ejecutable
    if getattr(sys, 'frozen', False):
        # Si es un ejecutable, buscar .env en el directorio del ejecutable
        exe_dir = Path(sys.executable).parent
        env_file = exe_dir / ".env"
        if env_file.exists():
            # Configurar la variable de entorno para que dotenv lo encuentre
            # Esto permite que load_dotenv() lo encuentre sin cambiar el directorio de trabajo
            os.environ['DOTENV_FILE'] = str(env_file)
            print(f"Archivo .env encontrado en: {env_file}")
        else:
            print(f"ADVERTENCIA: Archivo .env no encontrado en: {env_file}")
            print(f"Por favor, copia el archivo .env al directorio del ejecutable.")
    
    # Asegurar que el directorio esté en sys.path para que los módulos se puedan importar
    if str(app_path) not in sys.path:
        sys.path.insert(0, str(app_path))
    
    print("Iniciando aplicacion Streamlit...")
    print(f"Directorio: {app_path}")
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        print(f"Ejecutando desde ejecutable (directorio temporal: {sys._MEIPASS})")
    print("La aplicacion se abrira automaticamente en tu navegador cuando este lista...")
    print("Para cerrar, presiona Ctrl+C en esta ventana\n")
    
    # Ejecutar Streamlit
    try:
        # Workaround para el problema de metadatos en PyInstaller
        # Necesitamos configurar el path de distribución antes de importar Streamlit
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Agregar el directorio de distribución a sys.path
            import site
            dist_path = Path(sys._MEIPASS)
            # Buscar directorios .dist-info en _MEIPASS
            for dist_info_dir in dist_path.glob("*.dist-info"):
                # Agregar el directorio padre al path
                site.addsitedir(str(dist_info_dir.parent))
        
        # Configurar developmentMode antes de importar Streamlit
        # Esto evita el conflicto con server.port
        os.environ['STREAMLIT_SERVER_PORT'] = '8501'
        os.environ['STREAMLIT_GLOBAL_DEVELOPMENT_MODE'] = 'false'
        
        print("Iniciando Streamlit... Por favor espera unos segundos...")
        print()
        
        # Importar el módulo CLI de Streamlit
        from streamlit.web import cli as st_cli
        
        # Configurar sys.argv para que Streamlit reciba los argumentos correctos
        original_argv = sys.argv.copy()
        sys.argv = [
            "streamlit",
            "run",
            str(app_file),
            # El puerto se toma del streamlit.toml o de la variable de entorno
            "--browser.gatherUsageStats=false",
            "--server.address=localhost",
            "--server.headless=false"  # Permitir que Streamlit abra el navegador
        ]
        
        # Ejecutar Streamlit directamente
        st_cli.main()
        
        # Restaurar sys.argv original
        sys.argv = original_argv
        
    except KeyboardInterrupt:
        print("\n\nDeteniendo servidor...")
        print("Servidor detenido correctamente")
    except Exception as e:
        print(f"\nERROR al ejecutar la aplicacion: {str(e)}")
        import traceback
        traceback.print_exc()
        print("\nPresiona Enter para salir...")
        input()
        sys.exit(1)

if __name__ == "__main__":
    main()

