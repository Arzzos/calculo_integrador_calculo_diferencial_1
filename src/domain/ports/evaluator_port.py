# Define el puerto (interfaz) para la evaluación de expresiones matemáticas.
# El dominio usa esta interfaz para desacoplarse de la implementación concreta (SymPy).

from abc import ABC, abstractmethod   # ABC y abstractmethod para definir clases abstractas y métodos abstractos.
import numpy as np                    # Para tipado de arreglos.

class EvaluatorPort(ABC):
    """
    Puerto (interfaz) para la evaluación de expresiones matemáticas.
    Las clases concretas que implementen este puerto deben proveer los métodos definidos aquí.
    """

    @abstractmethod
    def validate_expression(self, expression: str) -> bool:
        """Valida si la expresión es sintácticamente correcta."""
        pass

    @abstractmethod
    def evaluate(self, expression: str, x_values: np.ndarray) -> np.ndarray:
        """
        Evalúa la expresión para un conjunto de valores de x.
        Retorna un array de y_values.
        Lanza InvalidExpressionError si la expresión no es válida.
        """
        pass

    @abstractmethod
    def get_latex(self, expression: str) -> str:
        """Retorna la representación LaTeX de la expresión (para visualización)."""
        pass