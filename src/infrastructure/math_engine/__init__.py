# Convierte el directorio 'math_engine' en un paquete Python.
# Exporta el adaptador SympyEvaluatorAdapter para que pueda ser importado desde otros módulos.

from .sympy_evaluator_adapter import SympyEvaluatorAdapter

__all__ = ["SympyEvaluatorAdapter"]