# Caso de uso: preparar los datos para el gráfico (puede incluir transformaciones adicionales).
# Por ahora, solo pasa los datos del DTO.

from typing import Dict, Any
from src.application.dtos import EvaluationResultDTO

class GeneratePlotDataUseCase:
    """
    Caso de uso: Preparar los datos para el gráfico.
    """

    def execute(self, result_dto: EvaluationResultDTO) -> Dict[str, Any]:
        """
        Toma el DTO de resultados y devuelve un diccionario con los datos listos para graficar.
        """
        return {
            "x": result_dto.x_values,
            "y": result_dto.y_values,
            "expression": result_dto.expression,
            "latex": result_dto.latex,
        }