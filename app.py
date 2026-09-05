# Punto de entrada de la aplicación. Este archivo es el que se ejecuta para lanzar la interfaz gráfica.

import sys                       # Módulo sys: proporciona acceso a variables y funciones del intérprete, como la ruta de búsqueda de módulos.
from pathlib import Path         # Path: permite manejar rutas de archivos de forma orientada a objetos y multiplataforma.

# Añade el directorio 'src' al path de Python para que los módulos internos puedan ser importados correctamente.
# Path(__file__) obtiene la ruta del archivo actual (app.py). .parent sube un nivel (a la raíz del proyecto).
# Luego se concatena con 'src' y se convierte a string, y se añade a sys.path para que Python busque allí los paquetes.
sys.path.append(str(Path(__file__).parent / "src"))

# Se importa la función 'main' desde el módulo streamlit_dashboard que se encuentra en infrastructure.ui.
# Esta función es la que inicia la aplicación Streamlit.
from infrastructure.ui.streamlit_dashboard import main

# Bloque que se ejecuta solo si este archivo es el punto de entrada (no si es importado como módulo).
# Esto es estándar en Python para permitir que el script sea ejecutable.
if __name__ == "__main__":
    main()  # Llama a la función principal que inicia la interfaz de Streamlit.