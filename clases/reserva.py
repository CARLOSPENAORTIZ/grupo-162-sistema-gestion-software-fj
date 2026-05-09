# clases/reserva.py

"""
Clase Reserva - Integra clientes y servicios
"""

from datetime import datetime, timedelta
from .entidad_base import EntidadBase
from .cliente import Cliente
from .servicio import Servicio
from excepciones import (
    ReservaInvalidaError,
    DatosIncorrectosError,
    OperacionNoPermitidaError
)
from utilidades import logger


class Reserva(EntidadBase):
    """
    Representa una reserva de servicio para un cliente.
    Maneja estados, validaciones y procesamiento con excepciones.
    """
    
    # Estados posibles de una reserva
    ESTADO_PENDIENTE = "PENDIENTE"
    ESTADO_CONFIRMADA = "CONFIRMADA"
    ESTADO_CANCELADA = "CANCELADA"
    ESTADO_COMPLETADA = "COMPLETADA"
    
    def __init__(self, cliente, servicio, parametros_servicio=None, fecha_inicio=None):
        """
        Constructor de Reserva
        
        Args:
            cliente (Cliente): Cliente que hace la reserva
            servicio (Servicio): Servicio reservado
            parametros_servicio (dict): Parámetros para calcular costo
            fecha_inicio (datetime): Fecha de inicio (default: ahora)
            
        Raises:
            ReservaInvalidaError: Si los datos son inválidos
        """
        super().__init__()
        
        # Atributos privados
        self.__cliente = None
        self.__servicio = None
        self.__parametros_servicio = parametros_servicio or {}
        self.__fecha_inicio = fecha_inicio or datetime.now()
        self.__fecha_fin = None
        self.__estado = self.ESTADO_PENDIENTE
        self.__costo_total = 0
        self.__notas = ""
        
        try:
            # Validar y asignar
            self.__validar_cliente(cliente)
            self.__validar_servicio(servicio)
            
            self.__cliente = cliente
            self.__servicio = servicio
            
            # Calcular costo inicial
            self.__calcular_costo()
            
            # Validar la reserva completa
            self.validar()
            
            logger.info(
                f"Reserva creada: {cliente.nombre} - {servicio.nombre} "
                f"(ID: {self.id}, Costo: ${self.__costo_total})"
            )
            
        except Exception as e:
            logger.error(f"Error al crear reserva: {e}")
            raise ReservaInvalidaError(f"No se pudo crear la reserva: {e}") from e
    
    # ==================== VALIDACIONES PRIVADAS ====================
    
    def __validar_cliente(self, cliente):
        """Valida que el cliente sea válido"""
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("Se requiere un objeto Cliente válido")
        
        try:
            cliente.validar()
        except Exception as e:
            raise ReservaInvalidaError(f"Cliente inválido: {e}")
    
    def __validar_servicio(self, servicio):
        """Valida que el servicio sea válido y esté disponible"""
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Se requiere un objeto Servicio válido")
        
        if not servicio.disponible:
            raise ReservaInvalidaError(f"El servicio '{servicio.nombre}' no está disponible")
        
        try:
            servicio.validar()
        except Exception as e:
            raise ReservaInvalidaError(f"Servicio inválido: {e}")
    
    def __calcular_costo(self):
        """Calcula el costo de la reserva según los parámetros"""
        try:
            self.__costo_total = self.__servicio.calcular_costo(**self.__parametros_servicio)
            logger.debug(f"Costo calculado para reserva {self.id}: ${self.__costo_total}")
        except Exception as e:
            raise ReservaInvalidaError(f"Error al calcular costo: {e}")
    
    # ==================== GETTERS ====================
    
    @property
    def cliente(self):
        """Obtener cliente (solo lectura)"""
        return self.__cliente
    
    @property
    def servicio(self):
        """Obtener servicio (solo lectura)"""
        return self.__servicio
    
    @property
    def estado(self):
        """Obtener estado actual"""
        return self.__estado
    
    @property
    def costo_total(self):
        """Obtener costo total"""
        return self.__costo_total
    
    @property
    def fecha_inicio(self):
        """Obtener fecha de inicio"""
        return self.__fecha_inicio
    
    @property
    def fecha_fin(self):
        """Obtener fecha de fin"""
        return self.__fecha_fin
    
    @property
    def notas(self):
        """Obtener notas"""
        return self.__notas
    
    @notas.setter
    def notas(self, valor):
        """Establecer notas adicionales"""
        self.__notas = str(valor) if valor else ""
    
    # ==================== MÉTODOS DE NEGOCIO ====================
    
    def confirmar(self):
        """
        Confirma la reserva.
        Solo se puede confirmar si está PENDIENTE.
        
        Raises:
            OperacionNoPermitidaError: Si no está en estado PENDIENTE
        """
        if self.__estado != self.ESTADO_PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self.__estado}"
            )
        
        try:
            # Validar que el servicio siga disponible
            if not self.__servicio.disponible:
                raise ReservaInvalidaError("El servicio ya no está disponible")
            
            self.__estado = self.ESTADO_CONFIRMADA
            logger.info(f"Reserva {self.id} confirmada para {self.__cliente.nombre}")
            
        except Exception as e:
            logger.error(f"Error al confirmar reserva {self.id}: {e}")
            raise
    
    def cancelar(self, motivo=""):
        """
        Cancela la reserva.
        Se puede cancelar si está PENDIENTE o CONFIRMADA.
        
        Args:
            motivo (str): Motivo de cancelación
            
        Raises:
            OperacionNoPermitidaError: Si ya está CANCELADA o COMPLETADA
        """
        if self.__estado in [self.ESTADO_CANCELADA, self.ESTADO_COMPLETADA]:
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva {self.__estado}"
            )
        
        try:
            self.__estado = self.ESTADO_CANCELADA
            if motivo:
                self.__notas = f"Cancelación: {motivo}"
            
            logger.warning(
                f"Reserva {self.id} cancelada. Motivo: {motivo or 'No especificado'}"
            )
            
        except Exception as e:
            logger.error(f"Error al cancelar reserva {self.id}: {e}")
            raise
    
    def completar(self):
        """
        Marca la reserva como completada.
        Solo se puede completar si está CONFIRMADA.
        
        Raises:
            OperacionNoPermitidaError: Si no está CONFIRMADA
        """
        if self.__estado != self.ESTADO_CONFIRMADA:
            raise OperacionNoPermitidaError(
                f"Solo se pueden completar reservas CONFIRMADAS. Estado actual: {self.__estado}"
            )
        
        try:
            self.__estado = self.ESTADO_COMPLETADA
            self.__fecha_fin = datetime.now()
            
            logger.info(
                f"Reserva {self.id} completada. "
                f"Duración: {self.__fecha_fin - self.__fecha_inicio}"
            )
            
        except Exception as e:
            logger.error(f"Error al completar reserva {self.id}: {e}")
            raise
    
    def procesar(self):
        """
        Procesa la reserva completa: confirma y completa.
        Demuestra el uso de try/except/else/finally.
        
        Returns:
            bool: True si se procesó exitosamente
        """
        archivo_temporal = None
        
        try:
            logger.info(f"Iniciando procesamiento de reserva {self.id}")
            
            # Intentar confirmar
            self.confirmar()
            
            # Simulación de procesamiento
            import time
            time.sleep(0.1)  # Simula procesamiento
            
            # Completar
            self.completar()
            
        except OperacionNoPermitidaError as e:
            logger.error(f"Operación no permitida: {e}")
            return False
            
        except ReservaInvalidaError as e:
            logger.error(f"Reserva inválida durante procesamiento: {e}")
            return False
            
        except Exception as e:
            logger.error(f"Error inesperado al procesar reserva {self.id}: {e}")
            return False
            
        else:
            # Solo se ejecuta si NO hubo excepciones
            logger.info(f"Reserva {self.id} procesada exitosamente")
            return True
            
        finally:
            # SIEMPRE se ejecuta (limpieza)
            logger.debug(f"Finalizando procesamiento de reserva {self.id}")
            # Aquí se cerrarían archivos, conexiones, etc.
    
    def recalcular_costo(self, nuevos_parametros):
        """
        Recalcula el costo con nuevos parámetros.
        Solo si la reserva está PENDIENTE.
        
        Args:
            nuevos_parametros (dict): Nuevos parámetros para el servicio
            
        Raises:
            OperacionNoPermitidaError: Si no está PENDIENTE
        """
        if self.__estado != self.ESTADO_PENDIENTE:
            raise OperacionNoPermitidaError(
                "Solo se puede recalcular el costo de reservas PENDIENTES"
            )
        
        try:
            costo_anterior = self.__costo_total
            self.__parametros_servicio = nuevos_parametros
            self.__calcular_costo()
            
            logger.info(
                f"Costo recalculado para reserva {self.id}: "
                f"${costo_anterior} → ${self.__costo_total}"
            )
            
        except Exception as e:
            logger.error(f"Error al recalcular costo: {e}")
            raise
    
    # ==================== MÉTODO ABSTRACTO IMPLEMENTADO ====================
    
    def validar(self):
        """
        Valida que la reserva sea correcta.
        Implementación del método abstracto de EntidadBase.
        
        Returns:
            bool: True si es válida
            
        Raises:
            ReservaInvalidaError: Si hay datos inválidos
        """
        if not self.__cliente or not self.__servicio:
            raise ReservaInvalidaError("Reserva incompleta: falta cliente o servicio")
        
        if self.__costo_total <= 0:
            raise ReservaInvalidaError("El costo de la reserva debe ser mayor a 0")
        
        return True
    
    # ==================== MÉTODOS DE INFORMACIÓN ====================
    
    def obtener_resumen(self):
        """
        Obtiene un resumen completo de la reserva
        
        Returns:
            dict: Diccionario con toda la información
        """
        return {
            'id': self.id,
            'cliente': self.__cliente.nombre,
            'cliente_email': self.__cliente.email,
            'servicio': self.__servicio.nombre,
            'estado': self.__estado,
            'costo_total': self.__costo_total,
            'fecha_inicio': self.__fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_fin': self.__fecha_fin.strftime('%Y-%m-%d %H:%M:%S') if self.__fecha_fin else 'N/A',
            'parametros': self.__parametros_servicio,
            'notas': self.__notas or 'Sin notas'
        }
    
    def __str__(self):
        """Representación en string de la reserva"""
        return (
            f"Reserva {self.id}: {self.__cliente.nombre} - {self.__servicio.nombre} "
            f"[{self.__estado}] ${self.__costo_total}"
        )
    
    def __repr__(self):
        """Representación técnica de la reserva"""
        return (
            f"Reserva(id={self.id}, cliente={self.__cliente.id}, "
            f"servicio={self.__servicio.id}, estado={self.__estado})"
        )