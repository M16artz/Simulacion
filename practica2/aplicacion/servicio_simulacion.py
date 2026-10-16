import numpy as np

from fabrica.modelo_factory import ModeloFactory
from dominio.entidades import ParametrosSimulacion


class ServicioSimulacion:

    def __init__(self):
        self.datos = np.array(
            [1000, 1100, 1250, 1400, 1600, 1850, 2100],
            dtype=float
        )

    def establecer_datos(self, datos):
        valores = np.asarray(datos, dtype=float)

        if (
            valores.ndim != 1
            or len(valores) < 2
            or not np.all(np.isfinite(valores))
            or np.any(valores < 0)
        ):
            raise ValueError(
                "Ingrese al menos dos poblaciones "
                "válidas y no negativas."
            )

        self.datos = valores

    def calcular_tasa(self):
        """
        Ajusta log(P(t)/P0) = r*t por mínimos cuadrados usando todos
        los datos, con P0 fijo y observaciones separadas por una unidad.
        """
        inicial = self.datos[0]
        if np.any(self.datos <= 0):
            raise ValueError(
                "Todos los datos deben ser positivos para estimar la tasa "
                "exponencial. Para datos con ceros, indique r manualmente."
            )

        tiempos = np.arange(len(self.datos), dtype=float)
        log_relativo = np.log(self.datos) - np.log(inicial)
        return float(np.dot(tiempos, log_relativo) / np.dot(tiempos, tiempos))

    def ejecutar(self, tipo, parametros):
        modelo = ModeloFactory.crear(tipo)
        return modelo.simular(parametros)

    def comparar(self, parametros):
        resultados = {}

        for tipo in ModeloFactory.disponibles():
            resultados[tipo] = self.ejecutar(
                tipo,
                parametros
            )

        return resultados

    def crear_parametros(
        self,
        tasa=None,
        sigma=25.0,
        dt=0.1,
        semilla=42
    ):
        if tasa is None:
            tasa = self.calcular_tasa()

        return ParametrosSimulacion(
            poblacion_inicial=float(self.datos[0]),
            tasa=tasa,
            tiempo=len(self.datos) - 1,
            sigma=sigma,
            dt=dt,
            semilla=semilla
        )

    def resumen(self, resultados):
        print("\nRESULTADOS DE LA SIMULACIÓN")
        print("-" * 58)

        for resultado in resultados.values():
            print(
                f"{resultado.nombre:<23}"
                f"{resultado.poblacion_final:>12.2f}"
            )

        print("-" * 58)
        print(
            f"{'Dato real final':<23}"
            f"{self.datos[-1]:>12.2f}"
        )
