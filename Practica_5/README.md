# Práctica 5 – Laser Mapping

Esta practica implementa un sistema básico de mapeado láser mediante una estrategia de exploración aleatoria y construcción de un grid de ocupación a partir de los datos del sensor LIDAR.

El objetivo es que el robot recorra autónomamente un almacén mientras genera un mapa de los obstáculos presentes en el entorno.

La práctica se basa en construir un mapa probabilístico de ocupación a partir de las mediciones del sensor láser. Cada observación actualiza la probabilidad de que una celda esté libre u ocupada, permitiendo reconstruir progresivamente el entorno explorado.

## Descripción del Comportamiento

El robot ejecuta un bucle continuo con dos tareas principales:

1. **Construcción de un mapa de ocupación con LIDAR**
2. **Exploración aleatoria del entorno**

A continuación se detallan las etapas más relevantes.


## 1. **Inicialización del mapa**

Se inicializa un grid de ocupación probabilístico donde todas las celdas comienzan con una probabilidad de ocupación de 0.5 (estado desconocido).

```python
user_map = np.full((MAP_H, MAP_W), 0.5, dtype=float)
```

El mapa se envía a la GUI con:

```python
WebGUI.setUserMap(image)
```

## 2. **Obtención de posición y datos del láser**

En cada iteración del bucle de control se obtiene la posición actual del robot y las mediciones del sensor láser.

```python
pose = HAL.getPose3d()
rx, ry, ryaw = pose.x, pose.y, pose.yaw

laser_data = HAL.getLaserData()
laser = laser_data.values
```

La posición proporciona las coordenadas y orientación del robot en el entorno, mientras que el LIDAR devuelve una medida de distancia para cada dirección alrededor del robot.

Estas medidas permiten conocer tanto la ubicación desde la que se realiza la observación como la distancia a los posibles obstáculos detectados.

En esta implementación se utiliza la pose real proporcionada por el simulador (known position), por lo que no existe error de localización durante la construcción del mapa. Esto permite centrar el ejercicio en el proceso de mapeado a partir de las observaciones del sensor láser.

## 3. **Conversión de coordenadas al mapa**


Para representar la información del sensor en el mapa, las coordenadas del mundo real se transforman a coordenadas de píxel mediante la función proporcionada por el simulador. Tras realizar la conversión, se comprueba que la posición obtenida se encuentre dentro de los límites del mapa. Esta validación evita accesos fuera de rango y garantiza que las actualizaciones se realicen únicamente sobre celdas válidas del grid de ocupación. De este modo, las observaciones del robot pueden proyectarse correctamente sobre el mapa utilizado para la reconstrucción del entorno.

## 4. **Ray casting con linspace**

Para cada una de las medidas del láser, se calcula la posición del punto donde termina el rayo utilizando la distancia medida, la orientación del robot y el ángulo correspondiente.

A continuación, esa posición se transforma a coordenadas del mapa para obtener la celda final del rayo. Después, se recorren todas las celdas situadas entre la posición del robot y el punto final mediante la función de trazado de rayos implementada en el programa. Estas celdas se consideran espacio libre y su probabilidad de ocupación se reduce.

Si la medida corresponde realmente a un impacto contra un obstáculo (es decir, la distancia detectada es menor que el alcance máximo del sensor), la celda final del rayo se actualiza aumentando su probabilidad de estar ocupada.

Repitiendo este proceso para todos los rayos y para todas las observaciones del láser, el mapa probabilístico va incorporando evidencia sobre las zonas libres y ocupadas del entorno, permitiendo reconstruir progresivamente la distribución de obstáculos.


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

## Mapa de Ocupación

La matriz generada tiene dos tipos de celdas:

* **255 (blanco)** → Zona libre en la que el laser puede pasar sin obstaculos
* **127 (gris)** → Zona no explorada, ya sea porque hay obstaculo o porque aun no ha pasado.

## Modelo de actualización:

user_map[ey, ex] = min(
    1.0,
    user_map[ey, ex] * ratio_obstaculo
)

Mediante este modelo de actualización permitimos combinar las nuevas percepciones del sensor con las que ya hay en el mapa-

## Odometría

Como el entorno nos da el siguiente metodo para calcular la posición que no tiene ruido ya que no se usa odometria:

```python
pose = HAL.getPose3d()
```

para añadir odometría, se sustituiría la anterior linea por la siguiente:

```python
pose = HAL.getOdom()
```

Primero de todo el mapa con la posición real obtenida con getPose3D quedaría:

<img width="724" height="276" alt="Pose3D" src="https://github.com/user-attachments/assets/ffb2c95c-76f5-4f28-a76e-aaa7dcf546ab" />

Que con Odometría en el Universo de Small Laser Mapping Warehouse quedaría este mapa:

<img width="724" height="276" alt="Captura desde 2026-06-20 12-56-35" src="https://github.com/user-attachments/assets/283ffe2c-1221-454a-83c1-15e8fe10e54c" />

En cambio, en el universo de Small Laser Mapping Warehouse Medium Noise nos quedaría este mapa:

<img width="724" height="276" alt="MEDIORUYID" src="https://github.com/user-attachments/assets/3b42c3d9-4efd-4f30-9b47-755db09aa463" />

Y por útlimo, en el universo de Small Laser Mapping Warehouse High Noise tenemos este mapa:

<img width="738" height="290" alt="Mapa_High_Noise" src="https://github.com/user-attachments/assets/098b63e3-ac30-4f63-9fb3-bfec63803ee1" />

Más alla de analizar cual es el mapa más realista, se puede ver la cantidad de ruido viendo como difiere el rasto que deja la Odometria (azul) 
del rastro real (verde) viendo que cuanto más ruido más rapido va aumentando la diferencia y más difiere al final.

## Video de uso con Pose3D:

https://github.com/user-attachments/assets/46b88ec5-a31c-4f44-95b8-e76507e9c5ce

## Video de uso con ODOM:

https://github.com/user-attachments/assets/6f9f3cdf-3f70-444d-921d-b389a5efe244
