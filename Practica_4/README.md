# Práctica – Navegación Global mediante Wavefront BFS e Inflado de Obstáculos

Este proyecto implementa un sistema de navegación global basado en el algoritmo **Wavefront**, una técnica incluida dentro del método de **Gradient Path Planning (GPP)**.
El objetivo es que el robot alcance el destino seleccionado en el mapa siguiendo el gradiente descendente del campo de potencial, mientras evita colisiones gracias a un inflado artificial de los obstáculos.


## Descripción del Comportamiento

El robot ejecuta un bucle de control continuo que sigue estos pasos:


### 1. **Carga del mapa y preprocesado**

* Se obtiene la imagen del mapa con:

  ```python
  array = WebGUI.getMap('/resources/exercises/global_navigation/images/cityLargenBin.png')
  array = (array > 127).astype(np.uint8)
  ```

* Las celdas con valor `0` representan edificios y las `1` zonas transitables.

* Antes de planificar, los obstáculos se inflan para generar un “colchón” alrededor de ellos:

  ```python
  array = inflar_obstaculos(array, radio=2)
  ```

Esto reduce trayectorias peligrosamente cercanas a las paredes.

### 2. **Selección del destino**

* El usuario marca un punto en el mapa mediante la interfaz gráfica (`WebGUI.getTargetPose()`).
* El destino se convierte a coordenadas de la rejilla usando `WebGUI.rowColumn()`.

Cuando el destino cambia, se recalcula el campo de potencial.

### 3. **Cálculo del campo Wavefront BFS**

El algoritmo BFS se expande desde el destino, asignando valores crecientes a cada celda:

```python
campo = wavefront_bfs(goal_r, goal_c, robot_r, robot_c, expandir_extra=15)
WebGUI.showNumpy(campo)
```

Características principales:

* La expansión se detiene cuando alcanza el robot + un margen configurable.
* Las celdas infladas reciben un valor muy alto para desalentar su uso.
* El resultado es un mapa de potencial que forma un “camino en pendiente” hacia el destino.

### 4. **Selección del siguiente movimiento**

El robot busca, entre sus vecinos, aquellos cuya distancia potencial sea menor que la actual.
Para evitar atascos, se evalúan 1, 2 y 3 celdas hacia adelante en la misma dirección antes de tomar una decisión.

```python
if val != -1 and val < mejor_val:
    mejor_val = val
    mejor_dir = (dr, dc)
```

El vector elegido representa la dirección deseada de avance.

### 5. **Conversión a velocidades**

A partir del vector `(dx, dy)` seleccionado:

* Se obtiene el ángulo objetivo con `atan2`.
* Se compara con la orientación actual del robot.
* Se generan velocidades lineal y angular:

```python
HAL.setV(5)
HAL.setW(error_angle)
```

El robot avanza siempre “colina abajo” dentro del campo de potencial.

### 6. **Detección de llegada al destino**

Cuando el robot está suficientemente cerca del objetivo, se detiene:

```python
if abs(robot_r - goal_r) <= 2:
    HAL.setV(0)
    HAL.setW(0)
```

## Inflado de Obstáculos

El inflado consiste en ampliar artificialmente las zonas ocupadas marcando como peligrosas las celdas alrededor de cada edificio:

```python
for dr in range(-radio, radio + 1):
    for dc in range(-radio, radio + 1):
        nuevo[nr, nc] = 2
```

Esto produce rutas más suaves y evita que el robot roce esquinas o pasillos estrechos.


## Visualización

El campo generado por el algoritmo se muestra mediante la interfaz gráfica:

```python
WebGUI.showNumpy(campo)
```

La imagen resultante muestra:

* Celdas oscuras → zonas de alto coste (obstáculos inflados)
* Celdas claras → camino óptimo hacia el destino


## Problemas Detectados

* Si el destino se selecciona sobre una zona inflada, no es posible planificar y se pide escoger otra ubicación.
* En ocasiones, si el robot inicia fuera del campo BFS recalculado, pierde referencia hasta que se genera un nuevo destino.
* Algunos pasillos muy estrechos pueden quedar bloqueados debido al inflado de obstáculos y no poder seguir girando.


## Posibles Mejoras

* Ajuste dinámico del radio de inflado según la velocidad o el ángulo del robot.
* Añadir heurísticas para evitar zigzags en pasillos rectos.
* Integrar un módulo de replanificación continua para entornos dinámicos.
* Suavizado del campo de potencial para obtener trayectorias más fluidas.
* Combinación con algoritmos de navegación local (VFH, VFF, DWA).



