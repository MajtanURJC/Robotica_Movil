# Marker Based Visual Localization

Esta práctica implementa un sistema de **localización visual y navegación autónoma** de un robot móvil en un entorno 2D mediante la detección de marcadores visuales (AprilTags).  

El sistema estima la pose del robot usando visión por computador y utiliza dicha información para **moverse de forma autónoma**, buscando activamente nuevos marcadores.  

El robot se representa en tres formas:

- **Verde**: posición real
- **Azul**: posición según odometría (con ruido)
- **Rojo**: posición estimada mediante visión

## Descripción del Comportamiento

El sistema ejecuta un bucle continuo que integra **localización y navegación** en cada iteración.  
Tareas principales:

1. Detección de AprilTags y estimación de pose global
2. Navegación autónoma basada en visión
3. Visualización del estado del robot y del entorno

Ambos procesos se realizan **simultáneamente usando la misma observación visual**.


## Inicialización y configuración

Se importan las librerías necesarias y se configuran los parámetros:

```python
import cv2, HAL, WebGUI, pyapriltags, Frequency, numpy as np, yaml

Se inicializa el detector de AprilTags y se define el tamaño de los marcadores:

```python
detector = pyapriltags.Detector(families="tag36h11")
TAG_SIZE = 0.24
tag_object_points = ...  # puntos 3D del tag
tags_world = yaml.safe_load("apriltags_poses.yaml")
```

## Obtención de imágenes y ciclo de ejecución

El robot captura imágenes de la cámara, detecta tags, estima la pose y decide el movimiento en un bucle a frecuencia fija:

```python
Frequency.tick(20)
image = HAL.getImage()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
results = detector.detect(gray)
```


## Detección y visualización de AprilTags

Para cada tag detectado:

* Se dibuja su contorno y centro en la imagen.
* Se muestra su identificador (`tag_id`).
* Se calcula la pose relativa a la cámara.

**Todos los tags visibles se dibujan en pantalla**, aunque solo uno se use para navegación.

```python
for tag in results:
    dibujar(tag)
    if es_mas_cercano(tag):
        tag_seleccionado = tag
```

## Selección del tag de referencia

Se selecciona **un único tag por iteración** para:

* Navegación
* Estimación de pose global

Criterio de selección: "el tag más cercano a la cámara", garantizando estabilidad y coherencia.


## Transformaciones y estimación de pose del robot

Se calculan las transformaciones:

1. Tag → cámara
2. Cámara → robot
3. Mundo → tag

Combinando estas matrices se obtiene la pose global:

```python
world2robot = world2tag @ cam2tag @ cam2robot
x, y, yaw_robot = world2robot[0,3], world2robot[1,3], atan2(...)
WebGUI.showEstimatedPose((x, y, yaw_robot))
```

## Navegación autónoma basada en visión

El robot implementa un **comportamiento reactivo** guiado por los AprilTags:

* **Si no hay tags visibles**: gira explorando.
* **Si detecta un tag**: se orienta hacia él y avanza hasta una distancia mínima.
* **Cuando llega cerca**: deja de avanzar y gira para buscar otro tag.

```python
if tag_visible:
    v, w = calcular_velocidad(tag)
else:
    v, w = 0, exploracion_giro
HAL.setV(v)
HAL.setW(w)
```


## Visualización y control

Se actualiza continuamente:

* Imagen de la cámara con todos los tags detectados.
* Pose estimada del robot en el mapa.
* Movimiento del robot en el entorno.

```python
WebGUI.showImage(image)
WebGUI.showEstimatedPose((x, y, yaw_robot))
```

---

## Cámara y calibración

Se usa un modelo pinhole con parámetros intrínsecos del TurtleBot3:

```python
camera_matrix = np.array([...])
dist_coeffs = np.zeros((4,1))
```

Permite proyectar correctamente puntos 3D del mundo a coordenadas 2D de la imagen para estimar la pose.


## Posibles Mejoras

* Fusión de múltiples tags para robustez de la localización.
* Uso de filtros de Kalman para suavizar la estimación.
* Inclusión de sensores de distancia para evitar obstáculos.


```

