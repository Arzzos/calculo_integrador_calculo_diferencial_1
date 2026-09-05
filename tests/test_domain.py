# Módulo de pruebas unitarias para verificar el correcto funcionamiento de las clases del dominio.

import pytest                      # Framework de pruebas. Permite escribir pruebas de forma sencilla y ejecutarlas.
from src.domain.value_objects import Expression, Interval   # Importa los objetos de valor Expression e Interval.
from src.domain.entities import MathPoint, DomainRange, FunctionModel  # Importa entidades.

# Las funciones que comienzan con 'test_' son reconocidas por pytest como casos de prueba.

def test_expression_creation():
    # Prueba que se pueda crear una instancia de Expression con un valor válido.
    expr = Expression("x**2")       # Crea un objeto Expression con la cadena "x**2".
    assert expr.value == "x**2"     # Verifica que el atributo 'value' contenga exactamente esa cadena.

def test_expression_empty():
    # Prueba que al intentar crear una Expression con una cadena vacía, se lance una excepción ValueError.
    with pytest.raises(ValueError):  # Espera que se levante una excepción de tipo ValueError.
        Expression("")               # Intenta crear una expresión vacía; esto debe fallar.

def test_interval_validation():
    # Prueba la creación de un intervalo válido y que los límites sean correctos.
    interval = Interval(-1, 1)       # Crea un intervalo de -1 a 1.
    assert interval.min == -1        # Verifica el mínimo.
    assert interval.max == 1         # Verifica el máximo.
    with pytest.raises(ValueError):  # Se espera que al crear un intervalo con min > max se lance ValueError.
        Interval(1, -1)              # Intervalo inválido.

def test_domain_range():
    # Prueba la entidad DomainRange, que combina un intervalo y un número de puntos.
    interval = Interval(-1, 1)       # Crea el intervalo.
    dr = DomainRange(interval, 10)   # Crea un rango de dominio con 10 puntos.
    assert dr.num_points == 10       # Verifica que el número de puntos sea 10.
    with pytest.raises(ValueError):  # El número de puntos debe ser al menos 2; con 1 debe fallar.
        DomainRange(interval, 1)

def test_math_point():
    # Prueba la creación de un punto matemático (x, y).
    p = MathPoint(1.0, 2.0)          # Crea un punto con x=1.0, y=2.0.
    assert p.x == 1.0                # Verifica la coordenada x.
    assert p.y == 2.0                # Verifica la coordenada y.