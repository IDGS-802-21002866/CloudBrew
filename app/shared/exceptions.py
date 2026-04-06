class CloudBrewException(Exception):
    """Clase base para excepciones del sistema"""
    pass

class ValidacionNegocioException(CloudBrewException):
    """Excepción para reglas de negocio incumplidas"""
    pass