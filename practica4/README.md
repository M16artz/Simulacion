# Práctica 004 - SIR

## Python

Requisitos: Python 3.

Desde `practica4`, crear el entorno virtual:

```bash
python3 -m venv venv
```

Activarlo según el sistema operativo:

```bash
source venv/bin/activate
```

```powershell
venv\Scripts\Activate.ps1
```

Desde `practica4`, entrar a `python_sir`, instalar las dependencias y ejecutar:

```bash
cd python_sir
python -m pip install -r requirements.txt
python -m sir.presentacion.consola
```

La ejecución genera:

- `netlogo/resultados_python.csv`
- `netlogo/resultados_euler_python.csv`
- `results/grafica_python.png`

También se puede cambiar la semilla o las rutas de salida:

```bash
python -m sir.presentacion.consola --semilla 42 --csv ../netlogo/resultados_python.csv --grafica ../results/grafica_python.png
```

## NetLogo

1. Abrir `netlogo/SIR.nlogox` con NetLogo 7.x.
2. Pulsar `preparar`.
3. Pulsar `avanzar` y esperar a que la simulación llegue al paso 100.
4. Pulsar `exportar-netlogo` para generar `netlogo/resultados_netlogo.csv`.
5. Para comparar con Python, comprobar que exista `netlogo/resultados_python.csv`, pulsar `cargar-python` y después `actualizar-graficas-importadas`.

La interfaz incluye los botones `preparar`, `avanzar`, `cargar-python`, `exportar-netlogo` y `actualizar-graficas-importadas`, además de los gráficos `SIR NetLogo`, `SIR Python`, `Comparacion infectados`, `Comparacion susceptibles` y `Comparacion recuperados`.
