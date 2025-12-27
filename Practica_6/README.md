# Marker Based Visual Localization

Esta práctica implementa un sistema de localización visual de un robot en un entorno 2D mediante la detección de marcadores visuales (AprilTags).
El objetivo es estimar la pose (posición y orientación) del robot usando visión por computadora y métodos matemáticos para relacionar las etiquetas detectadas con sus posiciones conocidas en el mundo.

El robot se representa en tres formas:

- Verde: posición real.

- Azul: posición según odometría (con ruido).

- Rojo: posición estimada por el usuario.

#Descripción del Comportamiento

El sistema ejecuta un bucle continuo con dos tareas principales:

Detección de AprilTags y estimación de pose

Visualización de la pose estimada y control del robot

A continuación se detallan las etapas más relevantes.

1. Inicialización y configuración

Se importan las librerías necesarias y se configuran los parámetros:

import cv2, HAL, WebGUI, pyapriltags, Frequency, numpy as np, yaml, math


Se inicializa el detector de AprilTags:

detector = pyapriltags.Detector(searchpath=["apriltags"], families="tag36h11")
TAG_SIZE = 0.24
half = TAG_SIZE / 2


Se definen los puntos 3D de cada tag:

tag_object_points = np.array([
    [-half,  half, 0.0],
    [ half,  half, 0.0],
    [ half, -half, 0.0],
    [-half, -half, 0.0],
], dtype=np.float32)


Se cargan las posiciones conocidas de los tags desde un archivo YAML:

conf = yaml.safe_load(Path("/resources/exercises/marker_visual_loc/apriltags_poses.yaml").read_text())
tags_world = conf["tags"]

2. Obtención de imágenes y datos del robot

En cada iteración:

Frequency.tick(20)
image = HAL.getImage()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


Se usan funciones del HAL para controlar la velocidad del robot:

HAL.setV(0.1)
HAL.setW(0.2)


Se utiliza la GUI para mostrar imágenes y la pose estimada:

WebGUI.showImage(image)
WebGUI.showEstimatedPose((x, y, yaw_robot))

3. Detección de AprilTags

Se detectan los tags en la imagen:

results = detector.detect(gray)


Para cada tag detectado:

Se dibuja la caja delimitadora y el centro del tag en la imagen.

Se extrae el ID del tag para relacionarlo con su posición conocida.

Se calcula la pose del tag respecto a la cámara usando solvePnP:

success, rvec, tvec = cv2.solvePnP(tag_object_points, image_points, camera_matrix, dist_coeffs)

4. Transformaciones y estimación de pose del robot

Se construyen las matrices de transformación para convertir:

tag → cámara

cámara → robot

mundo → tag

Se combinan para obtener la pose del robot en el mundo:

world2robot = np.dot(np.dot(world2tag, cam2tag), cam2robot)
x, y = world2robot[0, 3], world2robot[1, 3]
yaw_robot = math.atan2(world2robot[1, 0], world2robot[0, 0]) + math.pi / 2

5. Visualización y control

El sistema actualiza continuamente:

Imagen con los tags detectados y sus bounding boxes.

Pose estimada del robot en el mapa.

Velocidad lineal y angular del robot.

6. Cámara y calibración

Se utiliza un modelo de cámara pinhole con parámetros intrínsecos:

camera_matrix = np.array([
    [focal, 0, cx],
    [0, focal, cy],
    [0, 0, 1]
], dtype=np.float64)
dist_coeffs = np.zeros((4, 1))


Estos parámetros permiten proyectar puntos 3D del mundo a coordenadas 2D de la imagen y son esenciales para la estimación precisa de la pose.

# Teoría

AprilTags: marcadores fiduciales robustos que permiten:

Alta fiabilidad de detección.

Resistencia a ruido, oclusión parcial y distorsión perspectiva.

Fácil decodificación para obtener el ID y posición conocida del tag.

PnP (Perspective-n-Point): permite estimar la pose del robot a partir de correspondencias 3D-2D entre los puntos del tag y la imagen.

# Posibles Mejoras

Integrar fusión odometría + visión para mayor precisión.

Uso de filtros de Kalman o SLAM visual para suavizar la estimación de pose.

Optimización de la detección de AprilTags con GPU o procesamiento paralelo.

Ajuste dinámico de la frecuencia de ejecución según la carga de procesamiento.
