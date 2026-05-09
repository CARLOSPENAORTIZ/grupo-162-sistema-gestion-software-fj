# excepciones/excepciones_personalizadas.py

"""
Excepciones personalizadas para el sistema de gestión
Software FJ
"""

class ErrorSistemaBase(Exception):
    """Excepción base para todas las excepciones del sistema"""
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class ClienteInvalidoError(ErrorSistemaBase):
    """Se lanza cuando los datos del cliente son inválidos"""
    pass


class ServicioNoDisponibleError(ErrorSistemaBase):
    """Se lanza cuando un servicio no está disponible"""
    pass


class ReservaInvalidaError(ErrorSistemaBase):
    """Se lanza cuando una reserva no puede procesarse"""
    pass


class DatosIncorrectosError(ErrorSistemaBase):
    """Se lanza cuando hay datos incorrectos en general"""
    pass


class OperacionNoPermitidaError(ErrorSistemaBase):
    """Se lanza cuando se intenta una operación no permitida"""
    pass