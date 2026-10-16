import numpy as np

from dominio.modelos.base import ModeloSimulacion
from dominio.entidades import ResultadoSimulacion


class ModeloDiscreto(ModeloSimulacion):

    def simular(self, parametros):
        if parametros.tasa < -1:
            raise ValueError("El modelo discreto requiere r >= -1 para evitar poblaciones negativas.")

        tiempos = np.arange(parametros.tiempo + 1)

        poblaciones = np.zeros(parametros.tiempo + 1)
        poblaciones[0] = parametros.poblacion_inicial

        for t in range(parametros.tiempo):
            poblacion_actual = poblaciones[t]

            incremento = parametros.tasa * poblacion_actual

            poblaciones[t + 1] = (
                poblacion_actual + incremento
            )

        return ResultadoSimulacion(
            nombre="Discreto",
            tiempos=tiempos,
            poblaciones=poblaciones
        )
