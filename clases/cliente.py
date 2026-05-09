# clases/cliente.py

"""
Clase Cliente con validaciones robustas y encapsulación
"""

from .entidad_base import EntidadBase
from excepciones import ClienteInvalidoError, DatosIncorrectosError
from    utilidades import logger
import re


class Cliente(EntidadBase):
    """
    Representa un cliente del sistema Software FJ.
    Incluye validaciones estrictas y encapsulación de datos personales.
    """
    
    def __init__(self, nombre, email, telefono="", documento=""):
        """
        Constructor del cliente
        
        Args:
            nombre (str): Nombre completo del cliente
            email (str): Email del cliente
            telefono (str, optional): Teléfono del cliente
            documento (str, optional): Documento de identidad
            
        Raises:
            ClienteInvalidoError: Si los datos son inválidos
        """
        super().__init__()  # Llama al constructor de EntidadBase
        
        # Atributos privados
        self.__nombre = ""
        self.__email = ""
        self.__telefono = ""
        self.__documento = ""
        
        # Usar setters para validar al crear
        try:
            self.nombre = nombre
            self.email = email
            self.telefono = telefono
            self.documento = documento
            
            # Validar todo junto
            self.validar()
            
            logger.info(f"Cliente creado: {nombre} (ID: {self.id})")
            
        except Exception as e:
            logger.error(f"Error al crear cliente: {e}")
            raise ClienteInvalidoError(f"No se pudo crear el cliente: {e}") from e
    
    # ==================== GETTERS Y SETTERS ====================
    
    @property
    def nombre(self):
        """Obtener nombre del cliente"""
        return self.__nombre
    
    @nombre.setter
    def nombre(self, valor):
        """
        Establecer nombre con validación
        
        Args:
            valor (str): Nombre del cliente
            
        Raises:
            DatosIncorrectosError: Si el nombre es inválido
        """
        if not valor or not isinstance(valor, str):
            raise DatosIncorrectosError("El nombre no puede estar vacío")
        
        if len(valor.strip()) < 3:
            raise DatosIncorrectosError("El nombre debe tener al menos 3 caracteres")
        
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', valor):
            raise DatosIncorrectosError("El nombre solo puede contener letras y espacios")
        
        self.__nombre = valor.strip()
    
    @property
    def email(self):
        """Obtener email del cliente"""
        return self.__email
    
    @email.setter
    def email(self, valor):
        """
        Establecer email con validación
        
        Args:
            valor (str): Email del cliente
            
        Raises:
            DatosIncorrectosError: Si el email es inválido
        """
        if not valor or not isinstance(valor, str):
            raise DatosIncorrectosError("El email no puede estar vacío")
        
        # Validación simple de email
        patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron_email, valor):
            raise DatosIncorrectosError("El formato del email es inválido")
        
        self.__email = valor.lower().strip()
    
    @property
    def telefono(self):
        """Obtener teléfono del cliente"""
        return self.__telefono
    
    @telefono.setter
    def telefono(self, valor):
        """
        Establecer teléfono con validación
        
        Args:
            valor (str): Teléfono del cliente
        """
        if not valor:
            logger.warning(f"Cliente {self.__nombre if self.__nombre else 'sin nombre'} sin teléfono")
            self.__telefono = ""
            return
        
        # Limpiar caracteres especiales
        telefono_limpio = re.sub(r'[^0-9+]', '', str(valor))
        
        if len(telefono_limpio) < 7:
            raise DatosIncorrectosError("El teléfono debe tener al menos 7 dígitos")
        
        self.__telefono = telefono_limpio
    
    @property
    def documento(self):
        """Obtener documento del cliente"""
        return self.__documento
    
    @documento.setter
    def documento(self, valor):
        """Establecer documento del cliente"""
        self.__documento = str(valor).strip() if valor else ""
    
    # ==================== MÉTODOS ====================
    
    def validar(self):
        """
        Valida que todos los datos del cliente sean correctos.
        Implementación del método abstracto de EntidadBase.
        
        Returns:
            bool: True si es válido
            
        Raises:
            ClienteInvalidoError: Si hay datos inválidos
        """
        if not self.__nombre or not self.__email:
            raise ClienteInvalidoError("Cliente inválido: nombre y email son obligatorios")
        
        return True
    
    def obtener_info(self):
        """
        Obtiene información completa del cliente
        
        Returns:
            dict: Diccionario con la información del cliente
        """
        return {
            'id': self.id,
            'nombre': self.__nombre,
            'email': self.__email,
            'telefono': self.__telefono if self.__telefono else 'No proporcionado',
            'documento': self.__documento if self.__documento else 'No proporcionado',
            'fecha_registro': self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __str__(self):
        """Representación en string del cliente"""
        return f"Cliente: {self.__nombre} ({self.__email}) - ID: {self.id}"
    
    def __repr__(self):
        """Representación técnica del cliente"""
        return f"Cliente(id={self.id}, nombre={self.__nombre}, email={self.__email})"