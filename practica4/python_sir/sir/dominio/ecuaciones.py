"""Ecuaciones diferenciales SIR"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DerivadasSIR:
    susceptibles: float
    infectados: float
    recuperados: float


def calcular_derivadas(susceptibles: float, infectados: float,
                       recuperados: float, beta: float, gamma: float) -> DerivadasSIR:
    poblacion = susceptibles + infectados + recuperados
    if poblacion <= 0:
        raise ValueError("La poblacion total debe ser positiva")
    contagios = beta * susceptibles * infectados / poblacion
    recuperaciones = gamma * infectados
    return DerivadasSIR(-contagios, contagios - recuperaciones, recuperaciones)


def numero_reproductivo_basico(beta: float, gamma: float) -> float:
    if gamma <= 0:
        raise ValueError("Gamma debe ser positiva")
    return beta / gamma
