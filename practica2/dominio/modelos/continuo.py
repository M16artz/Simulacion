import numpy as np

from dominio.modelos.base import ModeloSimulacion
from dominio.entidades import ResultadoSimulacion


class ModeloContinuo(ModeloSimulacion):

    def simular(self, parametros):
        if 1 + parametros.tasa * min(parametros.dt, parametros.tiempo) < 0:
            raise ValueError("Euler requiere 1 + r * paso >= 0; reduzca dt para evitar poblaciones negativas.")

        tiempos = [0.0]
        poblaciones = [parametros.poblacion_inicial]

        while tiempos[-1] < parametros.tiempo:
            tiempo_actual = tiempos[-1]
            poblacion_actual = poblaciones[-1]

            paso = min(
                parametros.dt,
                parametros.tiempo - tiempo_actual
            )

            cambio = parametros.tasa * poblacion_actual

            nueva_poblacion = (
                poblacion_actual + paso * cambio
            )

            siguiente_tiempo = tiempo_actual + paso
            if np.isclose(siguiente_tiempo, parametros.tiempo, rtol=0, atol=1e-12):
                siguiente_tiempo = float(parametros.tiempo)
            if siguiente_tiempo <= tiempo_actual:
                raise ValueError("dt es demasiado pequeño para avanzar en el tiempo.")
            tiempos.append(siguiente_tiempo)
            poblaciones.append(nueva_poblacion)

        return ResultadoSimulacion(
            nombre="Continuo (Euler)",
            tiempos=np.array(tiempos),
            poblaciones=np.array(poblaciones)
        )
