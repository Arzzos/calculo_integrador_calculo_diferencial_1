# Define un DTO para los datos de entrada del caso de uso de evaluación.

from dataclasses import dataclass

@dataclass(frozen=True)
class FunctionInputDTO:
    """DTO para los datos de entrada del caso de uso."""
    expression: str    # Expresión matemática en términos de 'x'.
    x_min: float       # Límite inferior del dominio.
    x_max: float       # Límite superior del dominio.
    num_points: int    # Número de puntos a evaluar.