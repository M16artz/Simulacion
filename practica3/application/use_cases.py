"""Casos de uso; no conocen HTTP ni elementos visuales."""
from dataclasses import asdict
from domain.models import Config
from domain.queueing import theoretical
from infrastructure.simpy_engine import MM1Engine

ESCENARIOS = [
    {'name': 'Estable', 'arrival_rate': 2.0, 'service_rate': 3.0},
    {'name': 'Mayor utilización', 'arrival_rate': 2.5, 'service_rate': 3.0},
    {'name': 'Cerca de saturación', 'arrival_rate': 2.9, 'service_rate': 3.0},
]


def simulate(configuracion: Config) -> dict:
    simulacion = MM1Engine().run(configuracion)
    return {'config': asdict(configuracion), 'theory': theoretical(configuracion).to_dict(), **simulacion}


def compare(duracion: float = 3000, semilla: int = 42) -> list:
    comparaciones = []
    for escenario in ESCENARIOS:
        configuracion = Config(escenario['arrival_rate'], escenario['service_rate'], duracion, semilla)
        resultado = simulate(configuracion)
        comparaciones.append({'scenario': escenario['name'], **escenario,
                     'theory': resultado['theory'], 'simulated': resultado['summary']})
    return comparaciones
