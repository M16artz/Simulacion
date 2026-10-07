import matplotlib.pyplot as plt


class Graficador:

    def graficarResultados(self, resultados):
        horas = []
        indices = []

        for resultado in resultados:
            horas.append(resultado["hora"])
            indices.append(resultado["indice"])

        plt.figure(figsize=(10, 5))

        plt.plot(
            horas,
            indices,
            marker="o",
            label="Índice de lluvia"
        )

        # Límites de clasificación
        plt.axhline(
            y=0.40,
            linestyle="--",
            label="Baja posibilidad (0.40)"
        )

        plt.axhline(
            y=0.60,
            linestyle="--",
            label="Lluvia probable (0.60)"
        )

        plt.axhline(
            y=0.75,
            linestyle="--",
            label="Lluvia (0.75)"
        )

        plt.title("Índice de posibilidad de lluvia")
        plt.xlabel("Hora")
        plt.ylabel("Índice")

        plt.ylim(0, 1)

        plt.grid(True)
        plt.legend()

        plt.show()