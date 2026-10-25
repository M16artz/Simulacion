import argparse
from sir.dominio.modelo import ConfiguracionSIR
from sir.dominio.ecuaciones import calcular_derivadas, numero_reproductivo_basico
from sir.aplicacion.solucion_diferencial import resolver_por_euler
from sir.aplicacion.simulador import SimuladorSIR
from sir.infraestructura.exportador_csv import exportar_csv
from sir.infraestructura.graficador import guardar_grafica


def principal() -> None:
    analizador = argparse.ArgumentParser(description="Práctica4: SIR Python/SimPy")
    analizador.add_argument("--csv", default="../netlogo/resultados_python.csv")
    analizador.add_argument("--grafica", "--plot", dest="grafica",
                            default="../results/grafica_python.png")
    analizador.add_argument("--semilla", "--seed", dest="semilla", type=int, default=42)
    argumentos = analizador.parse_args()

    configuracion = ConfiguracionSIR(semilla=argumentos.semilla)
    derivadas_iniciales = calcular_derivadas(
        configuracion.susceptibles_iniciales, configuracion.infectados_iniciales,
        configuracion.recuperados_iniciales, configuracion.beta, configuracion.gamma)
    print(f"Valores iniciales: S={configuracion.susceptibles_iniciales}, "
          f"I={configuracion.infectados_iniciales}, R={configuracion.recuperados_iniciales}")
    print(f"Derivadas iniciales: {derivadas_iniciales} | "
          f"R0={numero_reproductivo_basico(configuracion.beta, configuracion.gamma):.2f}")
    historial = SimuladorSIR(configuracion).ejecutar()
    assert len(historial) == configuracion.pasos + 1
    assert all(registro.total == configuracion.poblacion for registro in historial)
    exportar_csv(historial, argumentos.csv)
    guardar_grafica(historial, argumentos.grafica)
    # Exportacion matematica adicional: NO sustituye los conteos enteros de SimPy.
    from pathlib import Path
    import csv
    referencia = resolver_por_euler(configuracion)
    ruta_euler = Path(argumentos.csv).with_name("resultados_euler_python.csv")
    ruta_euler.parent.mkdir(parents=True, exist_ok=True)
    with ruta_euler.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(("tiempo", "susceptibles", "infectados", "recuperados"))
        for registro in referencia:
            escritor.writerow((registro.tiempo, f"{registro.susceptibles:.8f}",
                               f"{registro.infectados:.8f}", f"{registro.recuperados:.8f}"))
    print(f"SimPy: {len(historial)} filas, final={historial[-1]}")
    print(f"CSV: {argumentos.csv} | Gráfica: {argumentos.grafica}")


if __name__ == "__main__":
    principal()
