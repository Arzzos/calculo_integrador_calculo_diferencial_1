# Caso de uso: evaluar una función matemática en un dominio dado.

import numpy as np
from src.domain.ports import EvaluatorPort
from src.domain.exceptions import InvalidExpressionError
from src.application.dtos import FunctionInputDTO, EvaluationResultDTO

class EvaluateFunctionUseCase:
    """
    Caso de uso: Evaluar una función matemática en un dominio dado.
    Depende de un EvaluatorPort (inyectado).
    """

    def __init__(self, evaluator: EvaluatorPort):
        """
        Constructor que recibe una implementación del puerto EvaluatorPort.
        Esto permite inyectar diferentes adaptadores (por ejemplo, para pruebas).
        """
        self._evaluator = evaluator

    def execute(self, input_dto: FunctionInputDTO) -> EvaluationResultDTO:
        """
        Ejecuta la evaluación de la función.
        input_dto: objeto con los datos de entrada (expresión, x_min, x_max, num_points).
        Retorna un EvaluationResultDTO con los resultados.
        """
        # Validar la expresión usando el adaptador.
        if not self._evaluator.validate_expression(input_dto.expression):
            raise InvalidExpressionError("La expresion no es valida.")

        # Generar el arreglo de valores de x utilizando numpy.linspace.
        # linspace crea 'num_points' valores uniformemente espaciados entre x_min y x_max.
        x_values = np.linspace(input_dto.x_min, input_dto.x_max, input_dto.num_points)

        # Evaluar la expresión para esos valores de x.
        try:
            y_values = self._evaluator.evaluate(input_dto.expression, x_values)
        except Exception as e:
            # Si ocurre algún error en la evaluación, se lanza una excepción personalizada.
            raise InvalidExpressionError(f"Error al evaluar: {str(e)}")

        # Obtener la representación LaTeX de la expresión.
        latex = self._evaluator.get_latex(input_dto.expression)

        # Crear y retornar el DTO con los resultados.
        return EvaluationResultDTO(
            expression=input_dto.expression,
            x_values=x_values.tolist(),   # Convertir arreglo NumPy a lista de Python.
            y_values=y_values.tolist(),
            latex=latex
        )