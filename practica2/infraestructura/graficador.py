from pathlib import Path

import matplotlib

import matplotlib.pyplot as plt
import numpy as np


class Graficador:

    @staticmethod
    def comparar(resultados, datos_reales=None, ruta=None, mostrar=True):
        fig = plt.figure(figsize=(11, 6))

        estilos = {
            "deterministico": "-",
            "discreto": "--",
            "estocastico": "-.",
            "continuo": ":"
        }

        for tipo, resultado in resultados.items():
            plt.plot(
                resultado.tiempos,
                resultado.poblaciones,
                linestyle=estilos.get(tipo, "-"),
                linewidth=2,
                label=resultado.nombre
            )

        if datos_reales is not None:
            tiempos_reales = np.arange(
                len(datos_reales)
            )

            plt.scatter(
                tiempos_reales,
                datos_reales,
                color="black",
                marker="o",
                s=45,
                zorder=5,
                label="Datos observados"
            )

        plt.title("Comparación de modelos poblacionales")
        plt.xlabel("Tiempo")
        plt.ylabel("Población")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        return Graficador._finalizar(fig, ruta, mostrar)

    @staticmethod
    def graficar_escenarios(
        servicio,
        tasas,
        sigma=25.0,
        dt=0.1,
        ruta=None,
        mostrar=True
    ):
        fig, ejes = plt.subplots(
            1, len(tasas),
            figsize=(7 * len(tasas), 5),
            squeeze=False
        )

        for indice, tasa in enumerate(tasas):
            parametros = servicio.crear_parametros(
                tasa=tasa,
                sigma=sigma,
                dt=dt
            )

            resultados = servicio.comparar(parametros)
            eje = ejes[0, indice]

            for resultado in resultados.values():
                eje.plot(
                    resultado.tiempos,
                    resultado.poblaciones,
                    label=resultado.nombre
                )

            eje.set_title(f"Tasa r = {tasa:.3f}")
            eje.set_xlabel("Tiempo")
            eje.set_ylabel("Población")
            eje.grid(True, alpha=0.3)
            eje.legend()

        plt.tight_layout()
        return Graficador._finalizar(fig, ruta, mostrar)

    @staticmethod
    def variabilidad_estocastica(
        servicio,
        sigmas=(0, 25, 75, 150),
        repeticiones=15,
        ruta=None,
        mostrar=True
    ):
        fig, ejes = plt.subplots(
            2, 2,
            figsize=(12, 8)
        )

        tasa = servicio.calcular_tasa()

        for eje, sigma in zip(ejes.flat, sigmas):
            for semilla in range(repeticiones):
                parametros = servicio.crear_parametros(
                    tasa=tasa,
                    sigma=sigma,
                    semilla=semilla
                )

                resultado = servicio.ejecutar(
                    "estocastico",
                    parametros
                )

                eje.plot(
                    resultado.tiempos,
                    resultado.poblaciones,
                    alpha=0.55
                )

            eje.set_title(f"Sigma = {sigma}")
            eje.set_xlabel("Tiempo")
            eje.set_ylabel("Población")
            eje.grid(True, alpha=0.3)

        plt.suptitle("Efecto de la aleatoriedad")
        plt.tight_layout()
        return Graficador._finalizar(fig, ruta, mostrar)

    @staticmethod
    def _finalizar(fig, ruta, mostrar):
        """Guarda en PNG automáticamente cuando el backend no es interactivo."""
        backend = str(matplotlib.get_backend()).lower()
        sin_interfaz = backend in {"agg", "pdf", "pgf", "ps", "svg", "template", "cairo"}
        if ruta is None and mostrar and sin_interfaz:
            titulo = fig._suptitle.get_text() if fig._suptitle else fig.axes[0].get_title()
            nombre = {
                "Comparación de modelos poblacionales": "comparacion_modelos",
                "Efecto de la aleatoriedad": "variabilidad_estocastica",
            }.get(titulo, "crecimiento_decrecimiento")
            ruta = Path("graficas") / f"{nombre}.png"
        if ruta is not None:
            ruta = Path(ruta)
            ruta.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(ruta, dpi=150, bbox_inches="tight")
            print(f"Gráfica guardada en: {ruta}")
        if mostrar and not sin_interfaz:
            plt.show()
        else:
            plt.close(fig)
        return fig
