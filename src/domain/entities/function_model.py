# Define la entidad FunctionModel que agrupa la expresión y su dominio.

from dataclasses import dataclass
from src.domain.value_objects import Expression, Interval

@dataclass(frozen=True)
class FunctionModel:
    """
    Entidad que agrupa la expresión matemática y el dominio (intervalo) sobre el cual se evalúa.
    """
    expression: Expression   # Objeto Expression que contiene la cadena de la función.
    domain: Interval         # Objeto Interval que define el dominio de evaluación.
    name: str = "f(x)"       # Nombre de la función (por defecto "f(x)").