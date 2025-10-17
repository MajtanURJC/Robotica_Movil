# Práctica – Seguimiento de Línea Roja (Follow Line)

Este proyecto implementa un **controlador PID** para un coche autónomo.  
El objetivo es que el vehículo siga una **línea roja** en el suelo de manera estable, ajustando su **velocidad lineal** y su **orientación angular** de forma automática mediante visión por computador.

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

## Parámetros Principales

| Tipo de Control | Kp | Ki | Kd |
|------------------|----|----|----|
| Angular (w) | 0.009 | 0.000015 | 0.0075 |
| Lineal (v) | 0.03 | 0.000015 | 0.015 |

* `Vmax = 11.0` → Velocidad máxima permitida.  
* `Vmin = 3.0` → Velocidad mínima de seguridad.  

Estos parámetros fueron ajustados experimentalmente para conseguir una respuesta estable y sin oscilaciones.

---

## Lógica de Prioridad

La prioridad principal es **mantener la línea dentro del campo de visión**.  
Si la línea no se detecta:

1. Se cancela cualquier control PID activo.
2. El coche gira lentamente sobre su eje para intentar recuperarla.
3. Se resetean los acumuladores integrales para evitar errores al retomar el control.

Esto garantiza que el vehículo pueda **relocalizar la trayectoria** sin comportamientos erráticos.

---

## Video corto demostración

<a href="https://jderobot.github.io/RoboticsAcademy/exercises/AutonomousCars/follow_line/">
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

Este proyecto demuestra el uso de **controladores PID** aplicados al seguimiento de trayectorias mediante **visión por computador**.  
El coche es capaz de seguir una línea roja con precisión, adaptando su velocidad y orientación de forma automática.  
Es un ejercicio ideal para comprender los fundamentos del **control en robótica móvil** y el uso de **procesamiento de imagen en tiempo real**.

---

