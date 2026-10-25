"""Referencia determinista: Euler con paso temporal de 1, separada de SimPy."""
from dataclasses import dataclass
from sir.dominio.modelo import ConfiguracionSIR
from sir.dominio.ecuaciones import calcular_derivadas


@dataclass(frozen=True)
class RegistroDiferencial:
    tiempo: int
    susceptibles: float
    infectados: float
    recuperados: float


def resolver_por_euler(configuracion: ConfiguracionSIR) -> list[RegistroDiferencial]:
    susceptibles = float(configuracion.susceptibles_iniciales)
    infectados = float(configuracion.infectados_iniciales)
    recuperados = float(configuracion.recuperados_iniciales)
    historial = [RegistroDiferencial(0, susceptibles, infectados, recuperados)]
    for tiempo in range(1, configuracion.pasos + 1):
        cambio = calcular_derivadas(susceptibles, infectados, recuperados,
                                   configuracion.beta, configuracion.gamma)
        susceptibles += cambio.susceptibles
        infectados += cambio.infectados
        recuperados += cambio.recuperados
        historial.append(RegistroDiferencial(tiempo, susceptibles, infectados, recuperados))
    return historial
