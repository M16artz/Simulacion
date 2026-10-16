from dataclasses import dataclass
from numbers import Real
import numpy as np


@dataclass(frozen=True)
class ParametrosSimulacion:
    poblacion_inicial: float
    tasa: float
    tiempo: int
    sigma: float = 25.0
    dt: float = 0.1
    semilla: int = 42

    def __post_init__(self):
        for nombre in ("poblacion_inicial", "tasa", "sigma", "dt"):
            valor = getattr(self, nombre)
            if not isinstance(valor, Real) or not np.isfinite(valor):
                raise ValueError(f"{nombre} debe ser un número real finito.")

        if isinstance(self.tiempo, (bool, np.bool_)) or not isinstance(self.tiempo, (int, np.integer)):
            raise ValueError("El tiempo debe ser un número entero.")

        if self.semilla is not None and (
            isinstance(self.semilla, (bool, np.bool_))
            or not isinstance(self.semilla, (int, np.integer))
            or self.semilla < 0
        ):
            raise ValueError("La semilla debe ser un entero no negativo o None.")

        if self.poblacion_inicial < 0:
            raise ValueError("La población no puede ser negativa.")

        if self.tiempo < 0:
            raise ValueError("El tiempo debe ser mayor o igual a 0.")

        if self.sigma < 0:
            raise ValueError("Sigma no puede ser negativo.")

        if self.dt <= 0:
            raise ValueError("dt debe ser mayor que 0.")


@dataclass
class ResultadoSimulacion:
    nombre: str
    tiempos: np.ndarray
    poblaciones: np.ndarray

    @property
    def poblacion_final(self) -> float:
        return float(self.poblaciones[-1])
