import numpy as np

from dominio.modelos.base import ModeloSimulacion
from dominio.entidades import ResultadoSimulacion


class ModeloEstocastico(ModeloSimulacion):

    def simular(self, parametros):
        generador = np.random.default_rng(
            parametros.semilla
        )

        tiempos = np.arange(parametros.tiempo + 1)

        poblaciones = np.zeros(parametros.tiempo + 1)
        poblaciones[0] = parametros.poblacion_inicial

        for t in range(parametros.tiempo):

            ruido = generador.normal(
                loc=0,
                scale=parametros.sigma
            )

            poblacion_actual = poblaciones[t]

            nueva_poblacion = (
                poblacion_actual
                + parametros.tasa * poblacion_actual
                + ruido
            )

            poblaciones[t + 1] = max(
                0,
                nueva_poblacion
            )

        return ResultadoSimulacion(
            nombre="Estocástico",
            tiempos=tiempos,
            poblaciones=poblaciones
        )