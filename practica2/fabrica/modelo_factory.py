from dominio.modelos.deterministico import ModeloDeterministico
from dominio.modelos.discreto import ModeloDiscreto
from dominio.modelos.estocastico import ModeloEstocastico
from dominio.modelos.continuo import ModeloContinuo


class ModeloFactory:

    _modelos = {
        "deterministico": ModeloDeterministico,
        "discreto": ModeloDiscreto,
        "estocastico": ModeloEstocastico,
        "continuo": ModeloContinuo
    }

    @classmethod
    def crear(cls, tipo):
        tipo = tipo.lower().strip()

        if tipo not in cls._modelos:
            raise ValueError(
                f"Modelo desconocido: {tipo}"
            )

        return cls._modelos[tipo]()

    @classmethod
    def disponibles(cls):
        return list(cls._modelos.keys())