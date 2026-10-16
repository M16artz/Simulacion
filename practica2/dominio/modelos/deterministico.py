import numpy as np

from dominio.modelos.base import ModeloSimulacion
from dominio.entidades import ResultadoSimulacion


class ModeloDeterministico(ModeloSimulacion):

    def simular(self, parametros):
        tiempos = np.arange(parametros.tiempo + 1)

        poblaciones = (
            parametros.poblacion_inicial
            * np.exp(parametros.tasa * tiempos)
        )

        return ResultadoSimulacion(
            nombre="Determinístico",
            tiempos=tiempos,
            poblaciones=poblaciones
        )