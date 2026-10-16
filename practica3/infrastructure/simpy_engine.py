"""Adaptador de SimPy: eventos y estadísticas observables de una sola estación FIFO."""
import random
import simpy
from domain.models import Config


class MM1Engine:
    def run(self, configuracion: Config) -> dict:
        configuracion.validate()
        generador_aleatorio = random.Random(configuracion.seed)
        entorno = simpy.Environment()
        servidor = simpy.Resource(entorno, capacity=1)
        eventos = []
        paquetes_llegados = paquetes_completados = 0
        espera_total = permanencia_total = servicio_total = 0.0
        area_cola = area_sistema = area_ocupacion = 0.0
        tiempo_anterior = 0.0
        longitud_cola_anterior = paquetes_sistema_anterior = ocupacion_anterior = 0
        muestras_espera = []
        paquetes = []

        def registrar_evento(tipo_evento, identificador_paquete=None, tiempo_espera=None, tiempo_servicio=None):
            nonlocal area_cola, area_sistema, area_ocupacion, tiempo_anterior
            nonlocal longitud_cola_anterior, paquetes_sistema_anterior, ocupacion_anterior
            intervalo_transcurrido = max(0.0, entorno.now - tiempo_anterior)
            area_cola += intervalo_transcurrido * longitud_cola_anterior
            area_sistema += intervalo_transcurrido * paquetes_sistema_anterior
            area_ocupacion += intervalo_transcurrido * ocupacion_anterior
            tiempo_anterior = float(entorno.now)
            longitud_cola_anterior = len(servidor.queue)
            ocupacion_anterior = int(servidor.count > 0)
            paquetes_sistema_anterior = paquetes_llegados - paquetes_completados
            tiempo_actual = float(entorno.now)
            eventos.append({
                't': round(tiempo_actual, 7), 'type': tipo_evento, 'id': identificador_paquete,
                'queue': longitud_cola_anterior, 'system': paquetes_sistema_anterior,
                'busy': ocupacion_anterior, 'arrived': paquetes_llegados, 'completed': paquetes_completados,
                'mean_wait': espera_total / paquetes_completados if paquetes_completados else 0.0,
                'mean_system': permanencia_total / paquetes_completados if paquetes_completados else 0.0,
                'mean_service': servicio_total / paquetes_completados if paquetes_completados else 0.0,
                'avg_queue': area_cola / tiempo_actual if tiempo_actual else 0.0,
                'avg_system': area_sistema / tiempo_actual if tiempo_actual else 0.0,
                'utilization': area_ocupacion / tiempo_actual if tiempo_actual else 0.0,
                'throughput': paquetes_completados / tiempo_actual if tiempo_actual else 0.0,
                'wait': tiempo_espera, 'service': tiempo_servicio,
            })

        def procesar_paquete(numero_paquete):
            nonlocal paquetes_llegados, paquetes_completados, espera_total, permanencia_total, servicio_total
            tiempo_llegada = entorno.now
            paquetes_llegados += 1
            with servidor.request() as solicitud:
                registrar_evento('arrival', numero_paquete)
                yield solicitud
                tiempo_espera = float(entorno.now - tiempo_llegada)
                tiempo_servicio = generador_aleatorio.expovariate(configuracion.service_rate)
                registrar_evento('service_start', numero_paquete, tiempo_espera=tiempo_espera, tiempo_servicio=tiempo_servicio)
                yield entorno.timeout(tiempo_servicio)
            # Tras liberar el recurso, contar la salida sin dobles conteos.
            paquetes_completados += 1
            espera_total += tiempo_espera
            permanencia_total += entorno.now - tiempo_llegada
            servicio_total += tiempo_servicio
            muestras_espera.append(tiempo_espera)
            paquetes.append({'id': numero_paquete, 'arrival': tiempo_llegada, 'start': tiempo_llegada + tiempo_espera,
                         'departure': float(entorno.now), 'wait': tiempo_espera, 'service': tiempo_servicio,
                         'system': float(entorno.now - tiempo_llegada)})
            registrar_evento('departure', numero_paquete, tiempo_espera=tiempo_espera, tiempo_servicio=tiempo_servicio)

        def generar_llegadas():
            numero_paquete = 0
            while True:
                intervalo_llegada = generador_aleatorio.expovariate(configuracion.arrival_rate)
                if entorno.now + intervalo_llegada >= configuracion.duration:
                    return
                yield entorno.timeout(intervalo_llegada)
                numero_paquete += 1
                entorno.process(procesar_paquete(numero_paquete))

        entorno.process(generar_llegadas())
        entorno.run(until=configuracion.duration)
        registrar_evento('end')
        return {
            'events': eventos,
            'jobs': paquetes,
            'summary': {
                'arrived': paquetes_llegados, 'completed': paquetes_completados,
                'pending': paquetes_llegados - paquetes_completados,
                'mean_wait': espera_total / paquetes_completados if paquetes_completados else 0,
                'mean_system': permanencia_total / paquetes_completados if paquetes_completados else 0,
                'mean_service': servicio_total / paquetes_completados if paquetes_completados else 0,
                'avg_queue': area_cola / configuracion.duration,
                'avg_system': area_sistema / configuracion.duration,
                'utilization': area_ocupacion / configuracion.duration,
                'throughput': paquetes_completados / configuracion.duration,
                'max_queue': max((evento['queue'] for evento in eventos), default=0),
                'wait_samples': muestras_espera,
            },
        }
