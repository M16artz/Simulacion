# Simulador de Lluvia — Práctica 1

Programa en Python que calcula un **índice de posibilidad de lluvia** a partir de
mediciones climáticas (hora, humedad, nubosidad y temperatura), clasifica el
resultado y lo muestra en una gráfica.

## Estructura del proyecto

```
practica1/
├── main.py           # Punto de entrada y menú interactivo
├── modelo.py         # Modelo de cálculo (normalización, factor de temperatura, índice)
├── presentacion.py   # Clasificación del índice (Sin lluvia, Baja posibilidad, ...)
├── graficador.py     # Gráfica del índice con matplotlib
├── requirements.txt  # Dependencias del proyecto
└── README.md         # Este archivo
```

---

## 1. Requisitos previos

- **Python 3.10 o superior** (Preferible Python 3.14).
- Comprobar la instalación:

```bash
python3 --version
```

---

## 2. Crear el entorno virtual

Desde la carpeta del proyecto:

```bash
cd ~/Documents/Simulacion/practica1

# Crear el entorno virtual (carpeta .venv)
python3 -m venv .venv
```

### Activar el entorno virtual

**Linux / macOS:**

```bash
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**

```bat
.venv\Scripts\activate.bat
```

Al activarse, el inicio de la terminal cambiará a `(.venv)`, lo que indica que
estás usando el entorno aislado del proyecto.

---

## 3. Instalar dependencias

Con el entorno virtual **activado**:

```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar las dependencias desde requirements.txt
python -m pip install -r requirements.txt
```

Para comprobar que todo quedó instalado:

```bash
python -m pip list
```

---

## 4. Ejecutar el proyecto

Con el entorno virtual activado, dentro de la carpeta del proyecto:

```bash
python main.py
```

Se mostrará el menú:

```
===== SIMULADOR DE LLUVIA =====
Coeficientes actuales: cH=0.5, cN=0.3, cT=0.2
1. Cargar mediciones de práctica
2. Ajustar modelo
3. Mostrar todas las mediciones
4. Restaurar coeficientes por defecto
5. Salir
Seleccione una opción:
```

---

## 5. Cómo usar el programa

| Opción | Descripción |
|--------|-------------|
| **1. Cargar mediciones de práctica** | Agrega las 9 mediciones de ejemplo (06:00 a 22:00), calcula el índice de cada una, muestra los resultados en pantalla y abre la gráfica. |
| **2. Ajustar modelo** | Permite ingresar nuevos valores para los coeficientes `cH` (humedad), `cN` (nubosidad) y `cT` (temperatura). |
| **3. Mostrar todas las mediciones** | Reprocesa y muestra todas las mediciones cargadas hasta el momento con los coeficientes actuales y grafica los resultados. |
| **4. Restaurar coeficientes por defecto** | Vuelve a los valores iniciales: `cH=0.5`, `cN=0.3`, `cT=0.2`. |
| **5. Salir** | Finaliza el programa. |

### Ejemplo de sesión

```bash
python main.py

# Dentro del programa:
# Seleccione una opción: 1        -> carga y grafica los datos de práctica
# Seleccione una opción: 2        -> cH: 0.6 / cN: 0.3 / cT: 0.1
# Seleccione una opción: 3        -> recalcula con los nuevos coeficientes
# Seleccione una opción: 4        -> restaura los coeficientes por defecto
# Seleccione una opción: 5        -> sale del programa
```

### Fórmula del índice

```
índice = cH * (humedad / 100) + cN * (nubosidad / 100) + cT * factorTemperatura
```

Donde `factorTemperatura` vale `1.0` si la temperatura es ≤ 10 °C, `0.1` si es
≥ 28 °C, y decrece linealmente entre ambos valores.

### Clasificación del resultado

| Índice | Estado |
|--------|--------|
| `< 0.40` | Sin lluvia |
| `0.40 – 0.60` | Baja posibilidad |
| `0.60 – 0.75` | Lluvia probable |
| `≥ 0.75` | Lluvia |

---

## 6. Desactivar el entorno virtual

Cuando termines de trabajar:

```bash
deactivate
```

---

## 7. Solución de problemas

**`ModuleNotFoundError: No module named 'matplotlib'`**
- No tienes el entorno virtual activado o no instalaste las dependencias.
  Repite los pasos 2 y 3.

**`python: command not found` o versión de Python incorrecta**
- Usa `python3` en lugar de `python`, o dentro del entorno virtual usa `python`.

**La ventana de la gráfica no aparece**
- `plt.show()` bloquea hasta que cierres la ventana. Si estás en un servidor
  o entorno sin escritorio, instala los backends necesarios:
  ```bash
  python -m pip install tkinter
  ```
  o ejecuta el programa en una máquina con entorno gráfico.

**Quieres volver a empezar desde cero**
```bash
deactivate
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```
