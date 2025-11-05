
# Práctica – Navegación Local mediante Campos de Fuerza Virtual (VFF)

Este proyecto desarrolla un sistema de navegación local basado en el método de Campos de Fuerza Virtual (VFF) para un vehículo robótico.
El propósito es que el coche alcance puntos objetivo intermedios (subgoals) evitando colisiones, combinando vectores de atracción y repulsión para determinar una trayectoria segura y eficiente.

---

## Descripción del Comportamiento

El robot ejecuta un bucle de control continuo que sigue estos pasos:

1. **Lectura de los sensores**

   * Se obtiene la posición y orientación actual del robot con `HAL.getPose3d()`.
   * Se adquieren los datos del escáner láser mediante `HAL.getLaserData()`.
   * El siguiente objetivo se solicita al sistema gráfico con `WebGUI.getNextTarget()`.

2. **Transformación de coordenadas**

   * La posición del objetivo se convierte al marco de referencia del robot usando `absolute2relative()` dado en el
     guión de la práctica.
   * Esto permite que el vector de atracción siempre se exprese en las coordenadas del coche.

3. **Procesamiento del escáner láser**

   * Los 180 valores de distancia se traducen a coordenadas polares y cartesianas mediante `parse_laser_data()` que
     también nos da el guión.
   * Se detecta el obstáculo más cercano dentro de un área de influencia y se calcula su vector de repulsión.
   * Se limita el vector de atracción porque sino es demasiado grande y siempre va a tener más fuerza que el de repulsión.

4. **Cálculo de la fuerza total**

   * El vector de atracción se limita para evitar magnitudes excesivas.
   * Los vectores de atracción y repulsión se combinan para obtener la fuerza resultante.
   * Dicha fuerza determina la dirección y la velocidad a la que el robot debe avanzar.

5. **Conversión a velocidades de movimiento**

   * La dirección de desplazamiento se calcula con `atan2(avg_y, avg_x)` y se asigna como velocidad angular `w`.
   * La componente X de la fuerza resultante define la velocidad lineal `v`.
   * Ambas se limitan para mantener un movimiento seguro:

     ```python
     w = max(-1.5, min(1.5, desired_angle))
     v = max(0.0, min(20, avg_x))
     HAL.setV(v)
     HAL.setW(w)
     ```

6. **Verificación de objetivos alcanzados**

   * Si la distancia entre el robot y el objetivo es menor a 2 metros, se marca el objetivo como alcanzado mediante `target.setReached(True)`.

---

## Procesamiento de Datos Láser

El robot dispone de un sensor láser frontal de 180°, cuyos datos se transforman en vectores relativos al robot:

```python
def parse_laser_data(laser_data):
    laser_polar = []
    laser_xy = []
    for i in range(180):
        dist = laser_data.values[i]
        angle = math.radians(i - 90)  # ángulo 0 al frente
        laser_polar.append((dist, angle))
        x = dist * math.cos(angle)
        y = dist * math.sin(angle)
        laser_xy.append((x, y))
    return laser_polar, laser_xy
```
---

## Cálculo del Vector de Repulsión

Se obtiene a partir del obstáculo más cercano dentro del rango de acción:

```python
def compute_repulsion_simple(laser_polar, laser_xy, influence=1.5, k=1.0):
    # Identifica el obstáculo más próximo
    # Calcula el vector unitario de repulsión con magnitud inversa a la distancia
    # Devuelve rx, ry
```

---

## Visualización

El módulo `WebGUI` permite representar en tiempo real las fuerzas calculadas:

* Atracción hacia el objetivo: verde
* Repulsión de los obstáculos:** rojo
* Fuerza total resultante: negro

```python
WebGUI.showForces([x_rel, y_rel], [rep_x, rep_y], [avg_x, avg_y])
WebGUI.showLocalTarget((tx, ty))
```

---

## Video

https://drive.google.com/file/d/1SbFnBCwSAHzE-8nxBXhlqlSYcgCJe22Q/view?usp=sharing

## Problemas Detectados

* En algunos casos, el coche tarda en planificar la trayectoria cuando el objetivo está justo frente a él, aunque finalmente lo logra.
* Ocasionalmente, el vehículo elige un camino demasiado estrecho en lugar de una ruta más amplia y segura.

---

## Posibles Mejoras

* Incluir el tratamiento de obstáculos dinámicos o móviles.
* Ajustar los parámetros de repulsión de forma adaptativa según la densidad de obstáculos.
* Aplicar un filtrado de vectores para reducir oscilaciones en pasillos angostos.
* Optimizar la combinación de fuerzas cuando existan múltiples obstáculos cercanos.
* Incorporar un mecanismo de recuperación en caso de que la fuerza resultante se anule.

