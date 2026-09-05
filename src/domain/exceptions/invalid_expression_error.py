# Define una excepción personalizada para errores de expresión inválida.

class InvalidExpressionError(Exception):
    """Excepción lanzada cuando la expresión matemática no es válida."""
    def __init__(self, message: str = "La expresion ingresada no es valida."):
        self.message = message
        super().__init__(self.message)   # Llama al constructor de la clase base Exception.