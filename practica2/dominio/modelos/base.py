from abc import ABC, abstractmethod

from dominio.entidades import (
    ParametrosSimulacion,
    ResultadoSimulacion
)


class ModeloSimulacion(ABC):

    @abstractmethod
    def simular(
        self,
        parametros: ParametrosSimulacion
    ) -> ResultadoSimulacion:
        """Ejecuta el modelo matemático."""
        pass