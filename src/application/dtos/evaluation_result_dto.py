# Define un DTO que contiene los resultados de la evaluación de la función.

from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class EvaluationResultDTO:
    """DTO que contiene los resultados de la evaluación."""
    expression: str          # Expresión original.
    x_values: List[float]    # Lista de valores de x evaluados.
    y_values: List[float]    # Lista de valores de f(x) correspondientes.
    latex: str               # Representación LaTeX de la expresión.