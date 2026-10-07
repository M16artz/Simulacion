class ClasificadorLluvia:

    def clasificar(self, indice):
        if indice < 0.40:
            return "Sin lluvia"

        elif indice < 0.60:
            return "Baja posibilidad"

        elif indice < 0.75:
            return "Lluvia probable"

        else:
            return "Lluvia"