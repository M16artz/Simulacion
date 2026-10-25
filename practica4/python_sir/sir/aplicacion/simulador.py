import random
import simpy

from sir.dominio.modelo import ConfiguracionSIR, EstadoSalud, RegistroSIR
from sir.dominio.reglas import probabilidad_infeccion


class SimuladorSIR:
    def __init__(self, configuracion: ConfiguracionSIR) -> None:
        self.configuracion = configuracion
        self.aleatorio = random.Random(configuracion.semilla)
        self.estados = (
            [EstadoSalud.INFECTADO] * configuracion.infectados_iniciales
            + [EstadoSalud.SUSCEPTIBLE] * (
                configuracion.susceptibles_iniciales
            )
        )
        self.aleatorio.shuffle(self.estados)
        self.historial: list[RegistroSIR] = []

    def _registrar(self, tiempo: int) -> None:
        self.historial.append(RegistroSIR(
            tiempo=tiempo,
            susceptibles=self.estados.count(EstadoSalud.SUSCEPTIBLE),
            infectados=self.estados.count(EstadoSalud.INFECTADO),
            recuperados=self.estados.count(EstadoSalud.RECUPERADO),
        ))

    def _avanzar_paso(self) -> None:
        estados_anteriores = self.estados.copy()
        cantidad_infectados = estados_anteriores.count(EstadoSalud.INFECTADO)
        probabilidad_contagio = probabilidad_infeccion(
            self.configuracion.beta,
            cantidad_infectados,
            self.configuracion.poblacion,
        )
        estados_siguientes = estados_anteriores.copy()
        for indice, estado in enumerate(estados_anteriores):
            if (estado is EstadoSalud.SUSCEPTIBLE
                    and self.aleatorio.random() < probabilidad_contagio):
                estados_siguientes[indice] = EstadoSalud.INFECTADO
            elif (estado is EstadoSalud.INFECTADO
                  and self.aleatorio.random() < self.configuracion.gamma):
                estados_siguientes[indice] = EstadoSalud.RECUPERADO
        self.estados = estados_siguientes

    def _proceso(self, entorno: simpy.Environment):
        self._registrar(0)
        for tiempo in range(1, self.configuracion.pasos + 1):
            yield entorno.timeout(1)
            self._avanzar_paso()
            self._registrar(tiempo)

    def ejecutar(self) -> list[RegistroSIR]:
        self.historial = []
        entorno = simpy.Environment()
        entorno.process(self._proceso(entorno))
        entorno.run()
        return self.historial
