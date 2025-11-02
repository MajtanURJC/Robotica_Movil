# Práctica – Navegación Local con Campos de Fuerza Virtual (VFF)

Este proyecto implementa un algoritmo de Campos de Fuerza Virtual (VFF) para un coche autónomo.
El objetivo es que el vehículo alcance objetivos específicos (mini targets) evitando obstáculos, sumando vectores de atracción y repulsión , y calculando la dirección resultante para moverse de manera segura.

---

## Descripción del Comportamiento

El robot realiza un bucle de control continuo con los siguientes pasos:

1. **Obtención de la pose y los sensores**

   * Se obtiene la posición y orientación del robot mediante `HAL.getPose3d()`.
   * Se leen los datos del sensor láser con `HAL.getLaserData()`.
   * Se obtiene el siguiente objetivo con `WebGUI.getNextTarget()`.

2. **Conversión de coordenadas absolutas a relativas**

   * La posición del objetivo se transforma al **sistema de coordenadas relativo al robot** con `absolute2relative()`.
   * Esto permite que el vector de atracción esté siempre en relación con la orientación actual del robot.

3. **Procesamiento de datos láser**

   * Los 180 valores de distancia se convierten a coordenadas **polares y cartesianas** mediante `parse_laser_data()`.
   * Se identifica el obstáculo más cercano dentro de un radio de influencia y se calcula un **vector de repulsión**.

4. **Cálculo de la fuerza resultante**

   * Se limita el vector de atracción para no superar valores máximos.
   * Se suma el **vector de atracción** y el **vector de repulsión** para obtener la **fuerza resultante**.
   * Esta fuerza determina la dirección del robot y su velocidad hacia adelante.

5. **Conversión a velocidades**

   * La dirección deseada se calcula con `atan2(avg_y, avg_x)` y se limita como velocidad angular `w`.
   * La componente X de la fuerza resultante se utiliza para calcular la velocidad lineal `v`.
   * Se aplican límites para asegurar velocidades seguras:

     ```python
     w = max(-1.5, min(1.5, desired_angle))
     v = 0.6 * max(0.0, min(1.2, forward_component))
     HAL.setV(v)
     HAL.setW(w)
     ```

6. **Marcado de objetivos alcanzados**

   * Si el robot se encuentra dentro de un radio de 2 metros del objetivo, se marca como alcanzado con `target.setReached(True)`.

---

## Procesamiento de Datos Láser

El robot usa un sensor láser de 180° hacia delante, y los datos se convierten en vectores polares y cartesianos relativos al robot:

```python
def parse_laser_data(laser_data):
    laser_polar = []
    laser_xy = []
    for i in range(180):
        dist = laser_data.values[i]
        angle = math.radians(i - 90)  # cero al frente
        laser_polar.append((dist, angle))
        x = dist * math.cos(angle)
        y = dist * math.sin(angle)
        laser_xy.append((x, y))
    return laser_polar, laser_xy
```

* Coordenadas polares: `(distancia, ángulo)`
* Coordenadas cartesianas: `(x, y)` relativas al robot

---

## Vector de Repulsión

Se calcula a partir del obstáculo más cercano dentro del rango de influencia:

```python
def compute_repulsion_simple(laser_polar, laser_xy, influence=1.5, k=1.0):
    # Se busca el obstáculo más cercano
    # Se calcula el vector unitario de repulsión y su magnitud inversamente proporcional a la distancia
    # Devuelve rx, ry
```

* Magnitud de la fuerza inversamente proporcional a la distancia al obstáculo.
* Orientación opuesta al obstáculo para evitar colisiones.

---

## Visualización

El módulo `WebGUI` permite mostrar en tiempo real:

* Fuerza del objetivo: verde
* Fuerza de obstáculos: rojo
* Fuerza resultante: negro


```python
WebGUI.showForces([x_rel, y_rel], [rep_x, rep_y], [avg_x, avg_y])
WebGUI.showLocalTarget((tx, ty))
```

---

## Posibles Mejoras

* Implementar manejo de **obstáculos en movimiento**.
* Ajustar dinámicamente los parámetros de repulsión según densidad de obstáculos.
* Evitar oscilaciones en corredores estrechos mediante filtrado de vectores.
* Optimizar el cálculo de la fuerza resultante para múltiples obstáculos cercanos.
* Implementar un sistema de recuperación si la suma de fuerzas es cero.

---

## Conclusión

Este proyecto demuestra la implementación de un algoritmo de navegación local basado en VFF.
El robot puede moverse hacia un objetivo, evitando obstáculos, sumando vectores de atracción y repulsión, y ajustando sus velocidades lineal y angular de manera segura y eficiente.
