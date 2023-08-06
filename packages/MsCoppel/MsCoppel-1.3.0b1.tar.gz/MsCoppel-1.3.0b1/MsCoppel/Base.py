from abc import abstractmethod, ABC

class Base(ABC):
    """
        Clase base para la implementacion de los tipos
        Worker y Fork
    """

    Topico = ''

    def __init__(self, Topico):
        self.Topico = Topico
    
    @abstractmethod
    def process(self, request, fnc, params=[]):
        """
            Metodo que se encargara de procesar los mensajes
            que se enviaran al microservicio.
        """
        return 0
    
    def confForks(self, conf):
        """
            Metodo para registrar la configuracion del metodo
            que se ejecutara.
        """
        pass
    
    def formatResponse(self, original, resp, errorCode = 0):
        """
            Metodo que se encarga de darle formato a la
            salida del procesamiento de la accion.
        """
        # Regresar la respuesta con el formato correcto 
        resp =  {
            "errorCode": errorCode,
            "response": {
                "data": original.get("data", None),
                "headers": original.get("headers", {}),
                "metadata": original.get("metadata", {}),
                "response": {
                    "data": {
                        "response": resp
                    },
                    "meta": {
                        "id_transaction": original["metadata"]["id_transaction"],
                        "status": 'ERROR' if errorCode < 0 else 'SUCCESS'
                    }
                },
                "uuid": original.get("uuid", None),
            }
        }

        # Retornar los datos
        return resp
