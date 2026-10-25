from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sir.dominio.modelo import RegistroSIR


def guardar_grafica(historial: list[RegistroSIR], ruta: str | Path) -> None:
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    tiempos = [registro.tiempo for registro in historial]
    for estado in ("susceptibles", "infectados", "recuperados"):
        plt.plot(tiempos, [getattr(registro, estado) for registro in historial],
                 label=estado.capitalize())
    plt.xlabel("Tiempo (pasos)")
    plt.ylabel("Número de personas")
    plt.title("Evolución del modelo SIR — Python/SimPy")
    plt.legend()
    plt.grid(alpha=0.2)
    plt.savefig(ruta, dpi=160, bbox_inches="tight")
    plt.close()
