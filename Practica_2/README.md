# Práctica – Seguimiento de Línea Roja (Follow Line)

Este proyecto implementa un **controlador PID** para un coche autónomo en el entorno de simulación de [Robotics Academy](https://jderobot.github.io/RoboticsAcademy/exercises/AutonomousCars/follow_line/).  
El objetivo es que el vehículo siga una **línea roja** en el suelo de manera estable y sin sobreoscilar, ajustando su **velocidad lineal** y su **orientación angular** mediante un controlador.

La lógica está programada en **Python**, utilizando los módulos `HAL`, `WebGUI`, `Frequency`, `cv2` y `numpy`.

---

## Descripción del Comportamiento

El robot realiza un bucle de control continuo con los siguientes pasos:

1. **Captura y procesamiento de imagen**

   * Obtiene la imagen desde la cámara del simulador con `HAL.getImage()`.
   * Convierte la imagen al espacio de color **HSV**.
   * Detecta la **línea roja** mediante dos máscaras de color (debido a las dos zonas del espectro rojo en HSV).
   * Calcula el **centroide** de la línea detectada usando momentos de imagen (`cv2.moments`).

2. **Cálculo del error y control de orientación (PID angular)**

   * Calcula el error horizontal como la diferencia entre el centro de la imagen y el centroide de la línea.
   * Aplica un **control PID** (con parámetros `Kp_w`, `Ki_w`, `Kd_w`) para ajustar la velocidad angular `w`.
   * Este control corrige la dirección del coche para mantener la línea centrada.

3. **Control de velocidad (PID lineal)**

   * Basado en el error angular, se ajusta la velocidad lineal `v`:
     - Si el error es pequeño → velocidad máxima (`Vmax`).
     - Si el error es grande → velocidad reducida.
   * Se usa otro controlador PID (`Kp_v`, `Ki_v`, `Kd_v`) con límites de seguridad (`Vmin`, `Vmax`).

4. **Comportamiento ante pérdida de línea**

   * Si no se detecta la línea roja, el coche:
     - Reduce la velocidad al mínimo.
     - Gira suavemente (`w = 0.3`) para intentar encontrar de nuevo la línea.
     - Reinicia los valores integrales del PID para evitar acumulaciones erróneas.

5. **Ejecución cíclica**

   * Cada ciclo actualiza las velocidades `v` y `w` mediante:
     ```python
     HAL.setV(v)
     HAL.setW(w)
     ```
   * Muestra la imagen procesada en la interfaz del simulador con `WebGUI.showImage()`.

---

## Captura y Procesamiento de la Imagen

El módulo `HAL` (Hardware Abstraction Layer) permite acceder a los sensores del simulador, entre ellos la **cámara frontal** del coche.

### Captura

La imagen se obtiene en formato **BGR (OpenCV)** con:
```python
img = HAL.getImage()
````

Después se obtienen sus dimensiones para después procesar solo la parte que nos interesa:

```python
height, width, _ = img.shape
```

Para reducir el ruido visual y centrarse en la línea, se procesa solo la mitad inferior:

```python
lower_half = img[height//2 : height, 0 : width]
```

### Conversión de color y detección de línea

1. Se convierte la imagen de **BGR a HSV**:

   ```python
   hsv = cv2.cvtColor(lower_half, cv2.COLOR_BGR2HSV)
   ```

2. Se definen dos rangos de color para detectar el **rojo**:

   ```python
   lower_red1 = np.array([0, 100, 100])
   upper_red1 = np.array([10, 255, 255])
   lower_red2 = np.array([160, 100, 100])
   upper_red2 = np.array([179, 255, 255])
   ```

3. Se combinan ambas máscaras:

   ```python
   mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
   mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
   mask = cv2.bitwise_or(mask1, mask2)
   ```

4. Se calculan los **momentos de la imagen** para obtener el **centroide** de la línea:

   ```python
   M = cv2.moments(mask)
   if M["m00"] > 0:
       cx = int(M["m10"] / M["m00"])
       cy = int(M["m01"] / M["m00"])
   ```

El punto cx representa la posición horizontal de la línea roja en la imagen, y es el que se usa como referencia para calcular el error del controlador.

---

## Parámetros Principales

| Tipo de Control | Kp    | Ki       | Kd     |
| --------------- | ----- | -------- | ------ |
| Angular (w)     | 0.009 | 0.000015 | 0.0075 |
| Lineal (v)      | 0.03  | 0.000015 | 0.015  |

* `Vmax = 10.0` → Velocidad máxima permitida.
* `Vmin = 3.0` → Velocidad mínima de seguridad.

Estos parámetros fueron ajustados experimentalmente para conseguir una respuesta estable y sin oscilaciones.

---

## Video corto demostración

<a href="https://drive.google.com/file/d/1tKGGAc3z75BNhvWXVCWrfPJbumqbZuDI/view?usp=sharing">
  <img 
    width="1717" 
    height="837" 
    alt="Simulador Follow Line" 
    src="https://jderobot.github.io/RoboticsAcademy/assets/follow_line.png" 
    style="cursor: pointer;"
  />
</a>

---

## Posibles Mejoras

* Implementar una **detección adaptativa del color rojo** según iluminación.
* Dividir la imagen en varias regiones para un **control más anticipativo**.
* Guardar los valores del error y la velocidad para graficar el comportamiento del PID.
* Ajustar dinámicamente los parámetros PID en función del tipo de curva.
* Implementar una rutina de recuperación más elaborada cuando se pierde completamente la línea.

---

## Conclusión

Este proyecto demuestra el uso de **controladores PID** aplicados al seguimiento de trayectorias.
El coche es capaz de seguir una línea roja, adaptando su velocidad y orientación mediante un controlador.

