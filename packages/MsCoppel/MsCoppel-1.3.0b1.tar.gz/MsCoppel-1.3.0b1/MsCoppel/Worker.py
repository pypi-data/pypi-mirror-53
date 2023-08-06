from .Base import Base
from .ErrorMs import ErrorMs
from .Util import getItemBy

class Worker(Base):
    """
        Clase que contiene la logica para el manejo de los
        worker.
    """

    def process(self, request, fnc, params=[]):
        """
            Metodo que se encarga de procesar, la accion
            que se asign al evento del microservicio.

            @params resquest peticion de datos
            @params fnc Funcion a ejecutar
        """
        try:
            # Parametros
            paramsInject = {}

            # Seleccion de parametros
            for i in params:
                if i == 'data':
                    paramsInject.update({ i: request.get('data') })
                elif i == 'authorizacion':
                    paramsInject.update({ i: request["headers"]["Authorizacion"] })
                elif i == 'uuid':
                    paramsInject.update({ i: getItemBy('metadata.uuid', request) })
                elif i == 'response':
                    paramsInject.update({ i: getItemBy('response.data.response', request) })

            # Ejecutar la funciona final
            RESP = fnc(**paramsInject)
            # Regresar la respuesta con el formato correcto
            return self.formatResponse(request, RESP)
        except ErrorMs as err:
            # Retornar el error
            return self.formatResponse(request, None, err.errorCode)

