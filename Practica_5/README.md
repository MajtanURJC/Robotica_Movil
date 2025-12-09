# Práctica 5 – Laser Mapping

Esta practica implementa un sistema básico de mapeado láser mediante una estrategia de exploración aleatoria y construcción de un grid de ocupación a partir de los datos del sensor LIDAR.

El objetivo es que el robot recorra autónomamente un almacén mientras genera un mapa de los obstáculos presentes en el entorno.

La práctica se basa estrictamente en convertir las mediciones del láser a coordenadas en el mapa y rellenar una matriz que represente zonas libres, ocupadas o desconocidas.

## Descripción del Comportamiento

El robot ejecuta un bucle continuo con dos tareas principales:

1. **Construcción de un mapa de ocupación con LIDAR**
2. **Exploración aleatoria del entorno**

A continuación se detallan las etapas más relevantes.

---

## 1. **Inicialización del mapa**

Se crea una matriz de tamaño fijo `970 x 1500`, tal como indica el enunciado:

```python
user_map = np.full((MAP_H, MAP_W), UNKNOWN, dtype=np.uint8)
```

Valores usados:

* `UNKNOWN = 127` → celdas no exploradas
* `FREE = 0` → espacio libre
* `OCCUPIED = 255` → obstáculo detectado

El mapa se envía a la GUI con:

```python
WebGUI.setUserMap(user_map)
```

---

## 2. **Obtención de posición y datos del láser**

En cada iteración del bucle:

```python
pose = HAL.getPose3d()
rx, ry, ryaw = pose.x, pose.y, pose.yaw

laser_data = HAL.getLaserData()
laser = laser_data.values
```

Se usa la **pose real** del robot (no odometría con ruido), ya que la práctica asume *known positions*.

---

## 3. **Conversión de coordenadas al mapa**

El robot convierte posiciones del mundo a píxeles del mapa con:

```python
p = WebGUI.poseToMap(x, y, yaw)
```

Y se valida que estén dentro de los límites:

```python
if 0 <= px < MAP_W and 0 <= py < MAP_H:
```

Esto permite marcar correctamente las celdas en el grid de ocupación.

---

## 4. **Ray casting con Bresenham**

Para cada rayo láser (0–359 grados):

1. Se calcula la posición del impacto:

```python
wx = rx + d * cos(...)
wy = ry + d * sin(...)
```

2. Se obtiene el píxel final del rayo:

```python
end_px = world_to_map(wx, wy)
```

3. Se trazan todas las celdas intermedias con **Bresenham**:

```python
for cx, cy in bresenham(rpx, rpy, ex, ey):
    user_map[cy, cx] = FREE
```

Esto marca como libres todas las posiciones entre el robot y el punto medido.

4. Si el rayo golpea un obstáculo:

```python
if hit:
    user_map[ey, ex] = OCCUPIED
```

Con esto se grafica el territorio.


## 5. **Exploración del entorno**

Para explorar se usa un comportamiento reactivo muy simple basado en distancias mínimas:

```python
front = min_dist(range(-20, 20), laser)
left  = min_dist(range(60, 120), laser)
right = min_dist(range(-120, -60), laser)
```

Reglas aplicadas:

### Si hay un obstáculo cerca delante:

```python
HAL.setV(0.0)
if left > right:
    HAL.setW(W_TURN_RIGHT)
else:
    HAL.setW(W_TURN_LEFT)
```

### Si hay espacio libre:

```python
HAL.setV(V_FORWARD)
HAL.setW(0.0)
```

El resultado es un robot que avanza y evita obstáculos girando en funcion de los obstaculos, cubriendo progresivamente todo el mapa.


## 6. **Visualización del mapa**

En cada iteración, el mapa actualizado se muestra en la interfaz:

```python
WebGUI.setUserMap(user_map)
```

# Mapa de Ocupación

La matriz generada tiene tres tipos de celdas:

* **255 (blanco)** → Obstáculo detectado por el láser
* **0 (negro)** → Zona libre por donde ha pasado un rayo
* **127 (gris)** → Aún no explorado



## Posibles Mejoras

* **Integrar SLAM** (GMapping, Hector SLAM, Karto…). Evitaría errores acumulados y permitiría usar solo odometría.


* **Fusión de sensores**
  Odometría + LIDAR para mejorar precisión en la ocupación.


