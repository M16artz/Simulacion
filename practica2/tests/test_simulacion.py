import os
import tempfile
import unittest
from pathlib import Path

os.environ['MPLBACKEND'] = 'Agg'

import numpy as np

from aplicacion.servicio_simulacion import ServicioSimulacion
from dominio.entidades import ParametrosSimulacion
from infraestructura.graficador import Graficador


class SimulacionTests(unittest.TestCase):
    def setUp(self):
        self.servicio = ServicioSimulacion()

    def test_parametros_invalidos(self):
        for campo in ('poblacion_inicial', 'tasa', 'sigma', 'dt'):
            for valor in (float('nan'), float('inf'), -float('inf'), 'abc'):
                with self.subTest(campo=campo, valor=valor), self.assertRaises(ValueError):
                    ParametrosSimulacion(**{'poblacion_inicial': 1000, 'tasa': .1, 'tiempo': 6} | {campo: valor})
        for tiempo in (1.5, float('nan'), True, -1):
            with self.assertRaises(ValueError):
                ParametrosSimulacion(1000, .1, tiempo)

    def test_no_negatividad(self):
        with self.assertRaises(ValueError):
            self.servicio.ejecutar('discreto', self.servicio.crear_parametros(tasa=-2))
        with self.assertRaises(ValueError):
            self.servicio.ejecutar('continuo', self.servicio.crear_parametros(tasa=-2, dt=1))
        for tipo, tasa, dt in [('discreto', -1, 1), ('continuo', -2, .25)]:
            resultado = self.servicio.ejecutar(tipo, self.servicio.crear_parametros(tasa=tasa, dt=dt))
            self.assertTrue(np.all(resultado.poblaciones >= 0))

    def test_ajuste_exponencial(self):
        self.servicio.establecer_datos(100 * np.exp(.2 * np.arange(7)))
        self.assertAlmostEqual(self.servicio.calcular_tasa(), .2)
        anterior = self.servicio.calcular_tasa()
        self.servicio.datos[3] *= 2
        self.assertNotAlmostEqual(self.servicio.calcular_tasa(), anterior)
        self.servicio.establecer_datos([100, 0, 200])
        with self.assertRaises(ValueError):
            self.servicio.calcular_tasa()
        self.servicio.comparar(self.servicio.crear_parametros(tasa=.1))

    def test_euler_y_ruido_cero(self):
        parametros = self.servicio.crear_parametros(sigma=0)
        resultados = self.servicio.comparar(parametros)
        np.testing.assert_array_equal(resultados['discreto'].poblaciones, resultados['estocastico'].poblaciones)
        self.assertEqual(len(resultados['continuo'].tiempos), 61)
        errores = []
        for dt in (1, .1, .01):
            resultado = self.servicio.ejecutar('continuo', self.servicio.crear_parametros(dt=dt))
            self.assertEqual(resultado.tiempos[-1], parametros.tiempo)
            errores.append(abs(resultado.poblacion_final - resultados['deterministico'].poblacion_final))
        self.assertGreater(errores[0], errores[1])
        self.assertGreater(errores[1], errores[2])

    def test_exportar_graficas(self):
        resultados = self.servicio.comparar(self.servicio.crear_parametros())
        with tempfile.TemporaryDirectory() as directorio:
            rutas = [Path(directorio) / f'{i}.png' for i in range(3)]
            Graficador.comparar(resultados, self.servicio.datos, ruta=rutas[0], mostrar=False)
            Graficador.graficar_escenarios(self.servicio, [.12, -.12], ruta=rutas[1], mostrar=False)
            Graficador.variabilidad_estocastica(self.servicio, ruta=rutas[2], mostrar=False)
            for ruta in rutas:
                self.assertEqual(ruta.read_bytes()[:8], b'\x89PNG\r\n\x1a\n')


if __name__ == '__main__':
    unittest.main()
