# utilidades/logger.py

"""
Sistema de logging para registrar eventos y errores
"""

import logging
from datetime import datetime

def configurar_logger():
    """
    Configura el sistema de logging para el proyecto
    Registra eventos en el archivo eventos.log
    """
    # Crear el logger
    logger = logging.getLogger('SoftwareFJ')
    logger.setLevel(logging.DEBUG)  # Captura todos los niveles
    
    # Evitar duplicación de handlers
    if logger.handlers:
        return logger
    
    # Formato del mensaje de log
    formato = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para archivo
    archivo_handler = logging.FileHandler('eventos.log', encoding='utf-8')
    archivo_handler.setLevel(logging.DEBUG)
    archivo_handler.setFormatter(formato)
    
    # Handler para consola (opcional, para ver en pantalla también)
    consola_handler = logging.StreamHandler()
    consola_handler.setLevel(logging.INFO)
    consola_handler.setFormatter(formato)
    
    # Agregar handlers al logger
    logger.addHandler(archivo_handler)
    logger.addHandler(consola_handler)
    
    return logger


# Crear instancia global del logger
logger = configurar_logger()