# clases/entidad_base.py

"""
Clase abstracta base para todas las entidades del sistema
"""

from abc import ABC, abstractmethod
from datetime import datetime
import uuid

class EntidadBase(ABC):
    """
    Clase abstracta que representa una entidad general del sistema.
    Todas las entidades principales heredarán de esta clase.
    """
    
    def __init__(self):
        """Constructor base que genera ID único y fecha de creación"""
        self.__id = str(uuid.uuid4())[:8]  # ID único de 8 caracteres
        self.__fecha_creacion = datetime.now()
    
    @property
    def id(self):
        """Getter para el ID (solo lectura)"""
        return self.__id
    
    @property
    def fecha_creacion(self):
        """Getter para la fecha de creación (solo lectura)"""
        return self.__fecha_creacion
    
    @abstractmethod
    def validar(self):
        """
        Método abstracto que debe ser implementado por las subclases.
        Valida que los datos de la entidad sean correctos.
        
        Returns:
            bool: True si es válido, False en caso contrario
        
        Raises:
            Excepción personalizada si hay datos inválidos
        """
        pass
    
    def __str__(self):
        """Representación en string de la entidad"""
        return f"{self.__class__.__name__}(ID: {self.__id})"
    
    def __repr__(self):
        """Representación técnica de la entidad"""
        return f"{self.__class__.__name__}(id={self.__id}, fecha={self.__fecha_creacion})"