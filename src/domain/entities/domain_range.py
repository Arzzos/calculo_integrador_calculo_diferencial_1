# Define la entidad DomainRange que representa el rango de evaluación del dominio.

from dataclasses import dataclass
from src.domain.value_objects import Interval

@dataclass(frozen=True)
class DomainRange:
    """
    Entidad que representa el rango de evaluación del dominio.
    Contiene un intervalo y el número de puntos a muestrear.
    """
    interval: Interval   # Objeto Interval que define los límites.
    num_points: int      # Cantidad de puntos a generar dentro del intervalo.

    def __post_init__(self):
        # Validación: se requieren al menos 2 puntos para tener una línea.
        if self.num_points < 2:
            raise ValueError("El numero de puntos debe ser al menos 2.")