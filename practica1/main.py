from modelo import MedicionClimatica, ModeloLluvia
from presentacion import ClasificadorLluvia
from graficador import Graficador


# Coeficientes por defecto
CH_DEFAULT = 0.5
CN_DEFAULT = 0.3
CT_DEFAULT = 0.2


def cargar_datos_practica():
    return [
        MedicionClimatica("06:00", 65, 40, 14),
        MedicionClimatica("08:00", 70, 50, 16),
        MedicionClimatica("10:00", 68, 45, 18),
        MedicionClimatica("12:00", 60, 30, 22),
        MedicionClimatica("14:00", 75, 70, 20),
        MedicionClimatica("16:00", 85, 85, 18),
        MedicionClimatica("18:00", 92, 95, 16),
        MedicionClimatica("20:00", 88, 90, 17),
        MedicionClimatica("22:00", 80, 75, 15),
    ]


def procesar_medicion(medicion, modelo, clasificador, cH, cN, cT):
    indice = modelo.calcularIndice(
        medicion.humedad,
        medicion.nubosidad,
        medicion.temperatura,
        cH,
        cN,
        cT
    )

    estado = clasificador.clasificar(indice)

    print("\n--- Resultado ---")
    print(f"Hora: {medicion.hora}")
    print(f"Humedad: {medicion.humedad}%")
    print(f"Nubosidad: {medicion.nubosidad}%")
    print(f"Temperatura: {medicion.temperatura} °C")
    print(f"Índice: {indice:.2f}")
    print(f"Estado: {estado}")

    return {
        "hora": medicion.hora,
        "indice": indice,
        "estado": estado
    }


def imprimirResultados(mediciones, modelo, clasificador, cH, cN, cT):
    print("\n===== RESULTADOS =====")

    print(
        f"Coeficientes actuales -> "
        f"cH: {cH}, cN: {cN}, cT: {cT}"
    )

    resultados = []

    for medicion in mediciones:
        resultado = procesar_medicion(
            medicion,
            modelo,
            clasificador,
            cH,
            cN,
            cT
        )

        resultados.append(resultado)

    graficador = Graficador()
    graficador.graficarResultados(resultados)


def actualizar_coeficientes():
    print("\n===== MODELO AJUSTADO =====")

    cH = float(input("Ingrese nuevo coeficiente de humedad cH: "))
    cN = float(input("Ingrese nuevo coeficiente de nubosidad cN: "))
    cT = float(input("Ingrese nuevo coeficiente de temperatura cT: "))

    return cH, cN, cT


def main():
    modelo = ModeloLluvia()
    clasificador = ClasificadorLluvia()

    mediciones = []

    # Empieza siempre con los coeficientes por defecto
    cH = CH_DEFAULT
    cN = CN_DEFAULT
    cT = CT_DEFAULT

    while True:
        print("\n===== SIMULADOR DE LLUVIA =====")

        print(
            f"Coeficientes actuales: "
            f"cH={cH}, cN={cN}, cT={cT}"
        )

        print("1. Cargar mediciones de práctica")
        print("2. Ajustar modelo")
        print("3. Mostrar todas las mediciones")
        print("4. Restaurar coeficientes por defecto")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":

            nuevas_mediciones = cargar_datos_practica()

            mediciones.extend(nuevas_mediciones)

            imprimirResultados(
                nuevas_mediciones,
                modelo,
                clasificador,
                cH,
                cN,
                cT
            )

        elif opcion == "2":

            cH, cN, cT = actualizar_coeficientes()

            print("\nCoeficientes actualizados correctamente.")
            print(f"cH = {cH}")
            print(f"cN = {cN}")
            print(f"cT = {cT}")

        elif opcion == "3":

            if len(mediciones) == 0:
                print("No existen mediciones registradas.")

            else:
                imprimirResultados(
                    mediciones,
                    modelo,
                    clasificador,
                    cH,
                    cN,
                    cT
                )

        elif opcion == "4":

            cH = CH_DEFAULT
            cN = CN_DEFAULT
            cT = CT_DEFAULT

            print("\nCoeficientes restaurados.")
            print(f"cH = {cH}")
            print(f"cN = {cN}")
            print(f"cT = {cT}")

        elif opcion == "5":
            print("Programa finalizado.")
            break

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()