from aplicacion.servicio_simulacion import ServicioSimulacion
from infraestructura.graficador import Graficador


def ejecutar_comparacion(servicio):
    parametros = servicio.crear_parametros()

    resultados = servicio.comparar(parametros)

    print(f"\nTasa estimada: {parametros.tasa:.6f}")
    print(f"Sigma: {parametros.sigma}")
    print(f"dt: {parametros.dt}")

    servicio.resumen(resultados)

    Graficador.comparar(
        resultados,
        servicio.datos
    )


def modificar_parametros(servicio):
    print("\nCONFIGURAR PARÁMETROS")

    tasa = float(input("Tasa de crecimiento r: "))
    sigma = float(input("Nivel de ruido sigma: "))
    dt = float(input("Paso de Euler dt: "))

    parametros = servicio.crear_parametros(
        tasa=tasa,
        sigma=sigma,
        dt=dt
    )

    resultados = servicio.comparar(parametros)

    servicio.resumen(resultados)
    Graficador.comparar(
        resultados,
        servicio.datos
    )


def ingresar_datos(servicio):
    entrada = input(
        "Ingrese las poblaciones separadas por comas: "
    )

    datos = [
        float(valor.strip())
        for valor in entrada.split(",")
    ]

    servicio.establecer_datos(datos)

    print("Datos actualizados correctamente.")


def mostrar_menu():
    print("\n" + "=" * 45)
    print(" SIMULACIÓN DE CRECIMIENTO POBLACIONAL")
    print("=" * 45)
    print("1. Comparar los cuatro modelos")
    print("2. Modificar parámetros")
    print("3. Comparar crecimiento y decrecimiento")
    print("4. Analizar nivel de aleatoriedad")
    print("5. Introducir nuevos datos")
    print("6. Ver datos actuales")
    print("0. Salir")


def main():
    servicio = ServicioSimulacion()

    while True:
        mostrar_menu()

        opcion = input("\nSeleccione una opción: ").strip()

        try:
            if opcion == "1":
                ejecutar_comparacion(servicio)

            elif opcion == "2":
                modificar_parametros(servicio)

            elif opcion == "3":
                Graficador.graficar_escenarios(
                    servicio,
                    tasas=[0.12, -0.12]
                )

            elif opcion == "4":
                Graficador.variabilidad_estocastica(
                    servicio
                )

            elif opcion == "5":
                ingresar_datos(servicio)

            elif opcion == "6":
                print("\nDatos:", servicio.datos)
                print(
                    "Tasa estimada:",
                    servicio.calcular_tasa()
                )

            elif opcion == "0":
                print("Programa finalizado.")
                break

            else:
                print("Opción no válida.")

        except ValueError as error:
            print(f"\nError: {error}")

        except OverflowError:
            print("\nError: los valores son demasiado grandes.")


if __name__ == "__main__":
    main()