


class MedicionClimatica:
    def __init__(self, hora, humedad, nubosidad, temperatura):
        self.hora = hora
        self.humedad = humedad
        self.nubosidad = nubosidad
        self.temperatura = temperatura

class ModeloLluvia:

    def normalizar(self, valor):
        return valor / 100

    def calcularFactorTemperatura(self, temperatura):
        if temperatura <= 10:
            return 1.0
        elif temperatura >= 28:
            return 0.1

        return 1.0-(((temperatura-10)/2)*0.1)

    def calcularIndice(self, humedad, nubosidad, temperatura,cH,cN,cT):
        h = self.normalizar(humedad)
        n = self.normalizar(nubosidad)
        tf = self.calcularFactorTemperatura(temperatura)

        indice = cH * h + cN * n + cT * tf

        return indice