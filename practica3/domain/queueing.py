"""Teoría M/M/1, válida en régimen estacionario si λ < μ."""
from .models import Config, Theory


def theoretical(configuracion: Config) -> Theory:
    configuracion.validate()
    tasa_llegadas, tasa_servicio = configuracion.arrival_rate, configuracion.service_rate
    utilizacion = tasa_llegadas / tasa_servicio
    if tasa_llegadas >= tasa_servicio:
        return Theory(utilizacion, None, None, None, None, False)
    capacidad_disponible = tasa_servicio - tasa_llegadas
    paquetes_medios_sistema = tasa_llegadas / capacidad_disponible
    longitud_media_cola = tasa_llegadas * tasa_llegadas / (tasa_servicio * capacidad_disponible)
    permanencia_media = 1 / capacidad_disponible
    espera_media = tasa_llegadas / (tasa_servicio * capacidad_disponible)
    return Theory(
        rho=utilizacion,
        L=paquetes_medios_sistema,
        Lq=longitud_media_cola,
        W=permanencia_media,
        Wq=espera_media,
        stable=True,
    )
