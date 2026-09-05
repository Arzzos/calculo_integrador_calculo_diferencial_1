# Define una excepción personalizada para valores fuera del dominio.

class OutOfDomainError(Exception):
    """Excepción lanzada cuando un valor está fuera del dominio definido."""
    def __init__(self, message: str = "El valor esta fuera del dominio."):
        self.message = message
        super().__init__(self.message)