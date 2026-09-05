# Define la entidad MathPoint que representa un punto en el plano cartesiano.

from dataclasses import dataclass

@dataclass(frozen=True)
class MathPoint:
    """Representa un punto (x, y) en el plano cartesiano."""
    x: float   # Coordenada x.
    y: float   # Coordenada y (f(x)).