class CloudBrewException(Exception):
    """Clase base para excepciones del sistema"""

    pass


class ValidacionNegocioException(CloudBrewException):
    """Excepción para reglas de negocio incumplidas"""

    pass


class EntidadNoEncontradaError(CloudBrewException):
    """Excepción cuando no se encuentra una entidad"""

    pass
