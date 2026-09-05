# Implementación concreta del puerto EvaluatorPort utilizando la librería SymPy.
# Se encarga de validar, evaluar y generar representación LaTeX de expresiones matemáticas.

import sympy as sp                # SymPy: librería de matemática simbólica.
import numpy as np                # NumPy: para operaciones con arreglos.
from typing import Union          # Para anotaciones de tipo (opcional).
from src.domain.ports import EvaluatorPort   # Importa la interfaz que debe implementar.
from src.domain.exceptions import InvalidExpressionError  # Excepción personalizada.

class SympyEvaluatorAdapter(EvaluatorPort):
    """
    Adaptador concreto que usa SymPy para validar y evaluar expresiones,
    y numpy.lambdify para evaluación numérica eficiente.
    """

    def __init__(self):
        # Símbolo 'x' que se usará en las expresiones. 'real=True' indica que es una variable real.
        self._symbol = sp.Symbol('x', real=True)
        # Lista de módulos para lambdify: incluye numpy y un diccionario con funciones matemáticas comunes.
        # Esto permite que lambdify convierta funciones como sin, cos, exp, etc., a sus equivalentes numéricos.
        self._modules = ['numpy', {
            'sin': np.sin,
            'cos': np.cos,
            'tan': np.tan,
            'exp': np.exp,
            'log': np.log,
            'sqrt': np.sqrt,
            'abs': np.abs,
            'pi': np.pi,
            'e': np.e
        }]

    def validate_expression(self, expression: str) -> bool:
        """
        Valida sintácticamente la expresión y que solo contenga la variable 'x'.
        Retorna True si es válida, False en caso contrario.
        """
        try:
            # sympify convierte la cadena en una expresión simbólica de SymPy.
            # evaluate=False evita que simplifique automáticamente, lo cual es útil para validación.
            expr = sp.sympify(expression, evaluate=False)
            # Obtener los símbolos (variables) presentes en la expresión.
            symbols = expr.free_symbols
            # Si hay símbolos, verificar que todos sean 'x'. Si hay otros, es inválida.
            if symbols and not all(s.name == 'x' for s in symbols):
                return False
            return True
        except (sp.SympifyError, SyntaxError, ValueError):
            # Si ocurre cualquier error al parsear, la expresión no es válida.
            return False

    def evaluate(self, expression: str, x_values: np.ndarray) -> np.ndarray:
        """
        Evalúa la expresión para un arreglo de valores de x.
        Retorna un arreglo de y_values del mismo tamaño.
        Lanza InvalidExpressionError si hay problemas.
        """
        try:
            # Limpiar la expresión: eliminar espacios en blanco al inicio y final.
            cleaned_expr = expression.strip()
            
            # Reemplazar 'pi' y 'e' por sus símbolos matemáticos (π y ℯ) para SymPy.
            # Esto es opcional pero ayuda a que SymPy reconozca las constantes.
            cleaned_expr = cleaned_expr.replace('pi', 'π')
            cleaned_expr = cleaned_expr.replace('e', 'ℯ')
            
            # Convertir la cadena en expresión simbólica.
            expr = sp.sympify(cleaned_expr, evaluate=False)
            
            # Verificar nuevamente que solo tenga la variable 'x'.
            symbols = expr.free_symbols
            if symbols and not all(s.name == 'x' for s in symbols):
                invalid_symbols = [s.name for s in symbols if s.name != 'x']
                raise InvalidExpressionError(
                    f"La expresion contiene variables no permitidas: {invalid_symbols}. "
                    "Solo se permite la variable 'x'."
                )
            
            # Si no tiene símbolos, es una función constante.
            if not symbols:
                # Se define una función lambda que devuelve el valor constante para cualquier x.
                # float(expr) convierte la constante a número flotante.
                # np.ones_like(x_values) crea un arreglo del mismo tamaño lleno de 1, y se multiplica por la constante.
                f = lambda x: float(expr) * np.ones_like(x)
                return f(x_values)
            
            # Si tiene símbolos (debe ser 'x'), se crea una función vectorizada con lambdify.
            # lambdify convierte la expresión simbólica en una función que puede evaluarse numéricamente con numpy.
            f = sp.lambdify(self._symbol, expr, modules=self._modules)
            
            # Evaluar la función para todos los valores de x_values.
            y = f(x_values)
            
            # Asegurar que y sea un arreglo de tipo float (por si acaso).
            return np.asarray(y, dtype=float)
            
        except sp.SympifyError as e:
            # Error al parsear la expresión.
            raise InvalidExpressionError(f"Error al parsear la expresion: {str(e)}")
        except Exception as e:
            # Cualquier otro error (por ejemplo, división por cero, etc.)
            raise InvalidExpressionError(f"Error al evaluar la expresion: {str(e)}")

    def get_latex(self, expression: str) -> str:
        """
        Retorna la representación LaTeX de la expresión para visualización.
        """
        try:
            cleaned_expr = expression.strip()
            # Reemplazar constantes.
            cleaned_expr = cleaned_expr.replace('pi', 'π')
            cleaned_expr = cleaned_expr.replace('e', 'ℯ')
            expr = sp.sympify(cleaned_expr, evaluate=False)
            # sp.latex genera la cadena LaTeX.
            return sp.latex(expr)
        except Exception:
            # Si falla, devolver la expresión original encerrada entre signos de dólar para que se renderice como texto.
            return f"${expression}$"