# clases/servicio.py

"""
Clase abstracta Servicio y servicios especializados
"""

from abc import abstractmethod
from .entidad_base import EntidadBase
from excepciones import ServicioNoDisponibleError, DatosIncorrectosError
from utilidades import logger


class Servicio(EntidadBase):
    """
    Clase abstracta que representa un servicio de Software FJ.
    Define la estructura común para todos los tipos de servicios.
    """
    
    def __init__(self, nombre, descripcion, precio_base, disponible=True):
        """
        Constructor base de servicio
        
        Args:
            nombre (str): Nombre del servicio
            descripcion (str): Descripción del servicio
            precio_base (float): Precio base del servicio
            disponible (bool): Si el servicio está disponible
        """
        super().__init__()
        
        self.__nombre = ""
        self.__descripcion = ""
        self.__precio_base = 0
        self.__disponible = disponible
        
        try:
            self.nombre = nombre
            self.descripcion = descripcion
            self.precio_base = precio_base
            
            self.validar()
            logger.info(f"Servicio creado: {nombre} (ID: {self.id})")
            
        except Exception as e:
            logger.error(f"Error al crear servicio: {e}")
            raise ServicioNoDisponibleError(f"No se pudo crear el servicio: {e}") from e
    
    # ==================== GETTERS Y SETTERS ====================
    
    @property
    def nombre(self):
        return self.__nombre
    
    @nombre.setter
    def nombre(self, valor):
        if not valor or len(str(valor).strip()) < 3:
            raise DatosIncorrectosError("El nombre del servicio debe tener al menos 3 caracteres")
        self.__nombre = str(valor).strip()
    
    @property
    def descripcion(self):
        return self.__descripcion
    
    @descripcion.setter
    def descripcion(self, valor):
        if not valor:
            raise DatosIncorrectosError("La descripción no puede estar vacía")
        self.__descripcion = str(valor).strip()
    
    @property
    def precio_base(self):
        return self.__precio_base
    
    @precio_base.setter
    def precio_base(self, valor):
        try:
            precio = float(valor)
            if precio <= 0:
                raise DatosIncorrectosError("El precio debe ser mayor a 0")
            self.__precio_base = precio
        except ValueError:
            raise DatosIncorrectosError("El precio debe ser un número válido")
    
    @property
    def disponible(self):
        return self.__disponible
    
    @disponible.setter
    def disponible(self, valor):
        self.__disponible = bool(valor)
    
    # ==================== MÉTODOS ABSTRACTOS ====================
    
    @abstractmethod
    def calcular_costo(self, **kwargs):
        """
        Calcula el costo del servicio según parámetros específicos.
        Debe ser implementado por cada tipo de servicio.
        
        Args:
            **kwargs: Parámetros variables según el tipo de servicio
            
        Returns:
            float: Costo calculado
        """
        pass
    
    @abstractmethod
    def descripcion_detallada(self):
        """
        Retorna una descripción detallada del servicio.
        Debe ser implementada por cada tipo de servicio.
        
        Returns:
            str: Descripción detallada
        """
        pass
    
    # ==================== MÉTODOS CONCRETOS ====================
    
    def validar(self):
        """Valida que el servicio tenga datos correctos"""
        if not self.__nombre or not self.__descripcion:
            raise ServicioNoDisponibleError("Servicio inválido: faltan datos obligatorios")
        
        if self.__precio_base <= 0:
            raise ServicioNoDisponibleError("El precio debe ser mayor a 0")
        
        return True
    
    def activar(self):
        """Activa el servicio"""
        self.__disponible = True
        logger.info(f"Servicio {self.__nombre} activado")
    
    def desactivar(self):
        """Desactiva el servicio"""
        self.__disponible = False
        logger.warning(f"Servicio {self.__nombre} desactivado")
    
    def __str__(self):
        estado = "Disponible" if self.__disponible else "No disponible"
        return f"{self.__nombre} - ${self.__precio_base} - {estado}"


# ==================== SERVICIOS ESPECIALIZADOS ====================

class ServicioSala(Servicio):
    """Servicio de reserva de salas - Costo por horas"""
    
    def __init__(self, nombre, descripcion, precio_base, capacidad, equipamiento=""):
        """
        Constructor de ServicioSala
        
        Args:
            capacidad (int): Cantidad de personas que soporta
            equipamiento (str): Equipamiento disponible
        """
        self.__capacidad = 0
        self.__equipamiento = equipamiento
        
        super().__init__(nombre, descripcion, precio_base)
        self.capacidad = capacidad
    
    @property
    def capacidad(self):
        return self.__capacidad
    
    @capacidad.setter
    def capacidad(self, valor):
        try:
            cap = int(valor)
            if cap <= 0:
                raise DatosIncorrectosError("La capacidad debe ser mayor a 0")
            self.__capacidad = cap
        except ValueError:
            raise DatosIncorrectosError("La capacidad debe ser un número entero")
    
    @property
    def equipamiento(self):
        return self.__equipamiento
    
    def calcular_costo(self, horas=1, descuento=0):
        """
        Calcula el costo de la sala por horas
        
        Args:
            horas (int): Cantidad de horas
            descuento (float): Porcentaje de descuento (0-100)
            
        Returns:
            float: Costo total
        """
        if horas <= 0:
            raise DatosIncorrectosError("Las horas deben ser mayor a 0")
        
        if not 0 <= descuento <= 100:
            raise DatosIncorrectosError("El descuento debe estar entre 0 y 100")
        
        costo = self.precio_base * horas
        costo_con_descuento = costo * (1 - descuento / 100)
        
        logger.debug(f"Costo sala {self.nombre}: {horas}h = ${costo_con_descuento}")
        return round(costo_con_descuento, 2)
    
    def descripcion_detallada(self):
        """Descripción completa de la sala"""
        equip = f"Equipamiento: {self.__equipamiento}" if self.__equipamiento else "Sin equipamiento especial"
        return f"""
        🏢 SALA: {self.nombre}
        📝 {self.descripcion}
        👥 Capacidad: {self.__capacidad} personas
        🔧 {equip}
        💰 Precio: ${self.precio_base}/hora
        """


class ServicioEquipo(Servicio):
    """Servicio de alquiler de equipos - Costo por días"""
    
    def __init__(self, nombre, descripcion, precio_base, tipo_equipo, cantidad_disponible=1):
        """
        Constructor de ServicioEquipo
        
        Args:
            tipo_equipo (str): Tipo de equipo (laptop, proyector, etc.)
            cantidad_disponible (int): Cantidad disponible
        """
        self.__tipo_equipo = tipo_equipo
        self.__cantidad_disponible = 0
        
        super().__init__(nombre, descripcion, precio_base)
        self.cantidad_disponible = cantidad_disponible
    
    @property
    def tipo_equipo(self):
        return self.__tipo_equipo
    
    @property
    def cantidad_disponible(self):
        return self.__cantidad_disponible
    
    @cantidad_disponible.setter
    def cantidad_disponible(self, valor):
        try:
            cant = int(valor)
            if cant < 0:
                raise DatosIncorrectosError("La cantidad no puede ser negativa")
            self.__cantidad_disponible = cant
        except ValueError:
            raise DatosIncorrectosError("La cantidad debe ser un número entero")
    
    def calcular_costo(self, dias=1, cantidad=1, seguro=False):
        """
        Calcula el costo del equipo por días
        
        Args:
            dias (int): Cantidad de días
            cantidad (int): Cantidad de equipos
            seguro (bool): Si incluye seguro (+10%)
            
        Returns:
            float: Costo total
        """
        if dias <= 0 or cantidad <= 0:
            raise DatosIncorrectosError("Días y cantidad deben ser mayor a 0")
        
        if cantidad > self.__cantidad_disponible:
            raise ServicioNoDisponibleError(
                f"Solo hay {self.__cantidad_disponible} unidades disponibles"
            )
        
        costo = self.precio_base * dias * cantidad
        
        if seguro:
            costo *= 1.10  # +10% por seguro
        
        logger.debug(f"Costo equipo {self.nombre}: {dias}d x{cantidad} = ${costo}")
        return round(costo, 2)
    
    def descripcion_detallada(self):
        """Descripción completa del equipo"""
        return f"""
        💻 EQUIPO: {self.nombre}
        📝 {self.descripcion}
        🏷️  Tipo: {self.__tipo_equipo}
        📦 Disponibles: {self.__cantidad_disponible} unidades
        💰 Precio: ${self.precio_base}/día
        """


class ServicioAsesoria(Servicio):
    """Servicio de asesorías especializadas - Costo por sesión"""
    
    def __init__(self, nombre, descripcion, precio_base, especialidad, duracion_sesion=60):
        """
        Constructor de ServicioAsesoria
        
        Args:
            especialidad (str): Área de especialidad
            duracion_sesion (int): Duración en minutos
        """
        self.__especialidad = especialidad
        self.__duracion_sesion = duracion_sesion
        
        super().__init__(nombre, descripcion, precio_base)
    
    @property
    def especialidad(self):
        return self.__especialidad
    
    @property
    def duracion_sesion(self):
        return self.__duracion_sesion
    
    def calcular_costo(self, sesiones=1, grupal=False):
        """
        Calcula el costo de la asesoría
        
        Args:
            sesiones (int): Cantidad de sesiones
            grupal (bool): Si es grupal (+50%)
            
        Returns:
            float: Costo total
        """
        if sesiones <= 0:
            raise DatosIncorrectosError("Las sesiones deben ser mayor a 0")
        
        costo = self.precio_base * sesiones
        
        if grupal:
            costo *= 1.50  # +50% por asesoría grupal
        
        logger.debug(f"Costo asesoría {self.nombre}: {sesiones} sesiones = ${costo}")
        return round(costo, 2)
    
    def descripcion_detallada(self):
        """Descripción completa de la asesoría"""
        return f"""
        🎓 ASESORÍA: {self.nombre}
        📝 {self.descripcion}
        🏆 Especialidad: {self.__especialidad}
        ⏱️  Duración: {self.__duracion_sesion} minutos
        💰 Precio: ${self.precio_base}/sesión
        """