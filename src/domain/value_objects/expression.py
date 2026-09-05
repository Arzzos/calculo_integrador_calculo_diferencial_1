# Define un Value Object que representa una expresión matemática en términos de 'x'.

from dataclasses import dataclass   # dataclass permite crear clases con atributos automáticos (__init__, __repr__, etc.).

@dataclass(frozen=True)  # frozen=True hace que la clase sea inmutable (no se pueden modificar atributos después de creada).
class Expression:
    """
    Value Object que representa una expresión matemática en términos de 'x'.
    La validación sintáctica se delega al adaptador (SymPy) en la capa de infraestructura.
    Aquí solo almacenamos la cadena.
    """
    value: str  # Atributo que contiene la expresión como cadena de texto.

    def __post_init__(self):
        """
        Método que se ejecuta después del inicializador (__init__) generado por dataclass.
        Se usa para validaciones adicionales. Como la clase es frozen, no se pueden asignar atributos
        directamente, pero se puede lanzar una excepción si el valor no es válido.
        """
        # Validación: la expresión no puede estar vacía o ser solo espacios en blanco.
        if not self.value or not self.value.strip():
            raise ValueError("La expresion no puede estar vacia.")