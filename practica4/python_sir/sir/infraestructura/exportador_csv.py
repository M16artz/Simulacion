import csv
from pathlib import Path
from sir.dominio.modelo import RegistroSIR

COLUMNAS = ["tiempo", "susceptibles", "infectados", "recuperados"]


def exportar_csv(historial: list[RegistroSIR], ruta: str | Path) -> None:
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(COLUMNAS)
        for registro in historial:
            escritor.writerow((registro.tiempo, registro.susceptibles,
                              registro.infectados, registro.recuperados))
