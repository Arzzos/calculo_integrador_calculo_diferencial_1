# Define un Value Object que representa un intervalo cerrado [min, max].

from dataclasses import dataclass

@dataclass(frozen=True)
class Interval:
    """
    Value Object que representa un intervalo cerrado [min, max].
    """
    min: float   # Límite inferior.
    max: float   # Límite superior.

    def __post_init__(self):
        # Validación: el mínimo no puede ser mayor que el máximo.
        if self.min > self.max:
            raise ValueError("El valor minimo no puede ser mayor que el maximo.")
        # Validación de tipos: deben ser números (int o float).
        if not (isinstance(self.min, (int, float)) and isinstance(self.max, (int, float))):
            raise TypeError("Los limites deben ser numeros.")