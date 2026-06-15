# Marker Based Visual Localization

Esta práctica implementa un sistema de localización visual y navegación autónoma de un robot móvil en un entorno 2D mediante la detección de marcadores visuales (AprilTags).  

El sistema estima la pose del robot usando visión por computador y utiliza dicha información para moverse de forma autónoma, buscando activamente nuevos marcadores.  

El robot se representa en tres formas:

- Verde: posición real
- Rojo: posición estimada mediante visión u odometría

## Descripción del Comportamiento

El sistema ejecuta un bucle continuo que integra localización y navegación en cada iteración.  
Tareas principales:

1. Detección de AprilTags
2. Si no se detectan AprilTags detección por odometría
3. Navegación autónoma basada en visión u odometría, dependiendo de la detección
4. Visualización de la posición del robot y del entorno


## Configuración

Se configuran los parámetros intrinsecos que tenemos gracias al manual de la camara y los extrinsecos que calculamos:

```python
detector = pyapriltags.Detector(families="tag36h11")
TAG_SIZE = 0.24
tag_object_points = ...  # puntos 3D del tag
tags_world = yaml.safe_load("apriltags_poses.yaml")
```

## Detección y visualización de AprilTags

Para cada tag detectado en las imagenes:

- Se dibuja su contorno y centro en la imagen.
- Se muestra su identificador (`tag_id`).
- Se calcula la pose relativa a la cámara.

Todos los tags visibles se dibujan en pantalla, aunque solo uno se use para navegación.

```python
for tag in results:
    dibujar(tag)
    if es_mas_cercano(tag):
        tag_seleccionado = tag
```
## Estimación de posición mediante odometría

Cuando no se detecta ningún AprilTag en la imagen, el sistema continúa estimando la posición del robot utilizando la información proporcionada por la odometría.

De esta forma, el robot puede seguir manteniendo una estimación de su pose incluso cuando pierde temporalmente la referencia visual de los marcadores.

Funcionamiento
Si existe un AprilTag visible:
    Calcular la posición global mediante visión
    Guardar la posición estimada como referencia

Si no existe ningún AprilTag visible:
    Obtener el desplazamiento realizado desde la última medida
    Actualizar la posición estimada utilizando la odometría
    Actualizar la orientación del robot

Este mecanismo permite mantener una localización continua durante los periodos en los que los marcadores no son visibles. Cuando un AprilTag vuelve a ser detectado, la posición estimada se corrige utilizando nuevamente la información visual, reduciendo así el error acumulado por la odometría.

## Selección del tag de referencia

Se selecciona un único tag por iteración para:

- Navegación
- Estimación de pose global

Criterio de selección: "el tag más cercano a la cámara", garantizando estabilidad y coherencia.


## Transformaciones y estimación de pose del robot

Se calculan las transformaciones:

1. Tag -> cámara
2. Cámara -> robot
3. Mundo-> tag

Combinando estas matrices se obtiene la pose global:

```python
world2robot = world2tag @ cam2tag @ cam2robot
x, y, yaw_robot = world2robot[0,3], world2robot[1,3], atan2(...)
WebGUI.showEstimatedPose((x, y, yaw_robot))
```

## Navegación autónoma basada en visión

El robot implementa un comportamiento reactivo guiado por los AprilTags:

- Si no hay tags visibles: gira explorando.
- Si detecta un tag: se orienta hacia él y avanza a una velocidad mientras sigue girando.
- Cuando deja de verlo deja de avanzar y solo gira hasta que ve otro.

```python
if tag_visible:
    v = 0.05
else:
    v = 0 #gira sobre si mismo hasta ver otro

HAL.setV(v)
HAL.setW(w)
```


## Visualización y control

Se actualiza continuamente:

- Imagen de la cámara con todos los tags detectados.
- Pose estimada del robot en el mapa.
- Movimiento del robot en el entorno.

```python
WebGUI.showImage(image)
WebGUI.showEstimatedPose((x, y, yaw_robot))
```

## Cámara y calibración

Se usa un modelo pinhole con parámetros intrínsecos del TurtleBot3:

```python
camera_matrix = np.array([...])
dist_coeffs = np.zeros((4,1))
```

Permite proyectar correctamente puntos 3D del mundo a coordenadas 2D de la imagen para estimar la pose.

## Video de demostración:
https://drive.google.com/file/d/1F6glYmKV85gaup4tWRrghPxFdanHveLy/view?usp=sharing

