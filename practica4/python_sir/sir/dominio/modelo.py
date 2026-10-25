from dataclasses import dataclass
from enum import Enum


class EstadoSalud(str, Enum):
    SUSCEPTIBLE = "S"
    INFECTADO = "I"
    RECUPERADO = "R"


@dataclass(frozen=True)
class ConfiguracionSIR:
    poblacion: int = 100
    infectados_iniciales: int = 5
    beta: float = 0.30
    gamma: float = 0.10
    pasos: int = 100
    semilla: int = 42

    @property
    def susceptibles_iniciales(self) -> int:
        return self.poblacion - self.infectados_iniciales

    @property
    def recuperados_iniciales(self) -> int:
        return 0

    def __post_init__(self) -> None:
        if self.poblacion < 1 or not 0 <= self.infectados_iniciales <= self.poblacion:
            raise ValueError("Población e infectados iniciales inválidos")
        if not 0 <= self.beta <= 1 or not 0 <= self.gamma <= 1:
            raise ValueError("Beta y gamma deben estar entre 0 y 1")
        if self.pasos < 0:
            raise ValueError("La cantidad de pasos no puede ser negativa")


@dataclass(frozen=True)
class RegistroSIR:
    tiempo: int
    susceptibles: int
    infectados: int
    recuperados: int

    @property
    def total(self) -> int:
        return self.susceptibles + self.infectados + self.recuperados
