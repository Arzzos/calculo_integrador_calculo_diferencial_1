# Este archivo convierte el directorio 'ui' en un paquete Python.
# Además, exporta la función 'main' para que pueda ser importada desde niveles superiores.

from .streamlit_dashboard import main  # Importa la función main del módulo streamlit_dashboard.

__all__ = ["main"]  # Define la lista de símbolos que se exportan cuando se usa "from package import *".
                    # En este caso, solo se expone 'main'.