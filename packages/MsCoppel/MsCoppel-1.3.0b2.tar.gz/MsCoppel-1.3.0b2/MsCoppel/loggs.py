import sys
import os
from .loggsWrapper import LoggerWrapper

def Loggs(name):
    """
        Metodo para generar un elemento de logger
        @params name Nombre del modulo/libreria
    """
    # Validar si proviene de un ambiente productivo.
    if not os.environ.get('LOGS_FLUENT', None) is None:
        return LoggerWrapper(name)
    elif os.environ.get('PRODUCTION', None) is None:
        from logbook import Logger, StreamHandler
        StreamHandler(sys.stdout).push_application()
        return Logger(name)
    else:
        return LoggerWrapper(name)
