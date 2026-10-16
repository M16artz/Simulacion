# Simulación de crecimiento poblacional

Ejecutar `python main.py` después de instalar `requirements.txt` en un entorno virtual.

La tasa se estima con todos los datos mediante mínimos cuadrados sobre
`log(P(t)) - log(P0) = r*t`, manteniendo `P0` igual al primer dato y suponiendo
observaciones separadas por una unidad de tiempo. Por ello la curva ajustada
no tiene que coincidir exactamente con la última observación. Todos los datos
deben ser positivos para estimar la tasa; si hay ceros, se puede indicar `r`
mediante la opción 2 del menú.

La misma tasa se usa en los cuatro modelos para comparar sus ecuaciones según
la guía. La tasa exponencial continua y la tasa relativa discreta tienen distinta
interpretación: una tasa discreta equivalente sería `exp(r) - 1`.

El modelo discreto requiere `r >= -1`. Euler requiere `1 + r*paso >= 0`;
para tasas negativas, reducir `dt` si se rechaza la simulación. Los parámetros
numéricos deben ser finitos y el tiempo debe ser un entero no negativo.

Matplotlib selecciona el backend disponible. Sin interfaz gráfica, las opciones
del menú guardan PNG en `graficas/`. Los métodos de `Graficador` también aceptan
`ruta="archivo.png"` y `mostrar=False` para exportar explícitamente.

Comprobar el proyecto con `python -m unittest discover -s tests -v`.
