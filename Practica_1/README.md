# Robótica Móvil

# Práctica 1

Este proyecto implementa un algoritmo de exploración autónoma para un robot simulado. 
El robot combina un movimiento en **espiral creciente** con rutinas de evasión al detectar colisiones mediante su sensor bumper.

La lógica está programada en Python usando los módulos `WebGUI`, `HAL` y `Frequency`.

---

## Descripción del Comportamiento

El robot sigue un ciclo de **tres estados principales**:

1. **Avanzar en espiral (State 1)**

   * El robot avanza hacia adelante mientras describe una espiral creciente.
   * La velocidad lineal (`V_FORWARD`) aumenta poco a poco en cada ciclo gracias a `INC_FACTOR`.
   * La velocidad angular (`TURN_SPEED`) genera el efecto de espiral.

2. **Girar 180° (State 2)**

   * Si el bumper detecta un choque, el robot gira sobre su eje aproximadamente 180 grados.
   * El tiempo de giro (`TURN_180_TIME`) se calcula en función de `TURN_SPEED` y se multiplica por un factor aleatorio (`0.7–1.3`) para evitar trayectorias repetitivas.

3. **Avanzar recto un tiempo aleatorio (State 3)**

   * Tras el giro, el robot avanza recto con una velocidad más alta (`V_FORWARD = 0.7`).
   * Este avance dura un tiempo aleatorio (`FORWARD_TIME`) entre 2 y 6 segundos.
   * Después, vuelve al movimiento en espiral.

El ciclo se repite indefinidamente, lo que permite cubrir más área y evitar atascos.

---

## Parámetros principales

* `V_FORWARD = 0.2` → Velocidad inicial hacia adelante en espiral. 
* `FORWARD_TIME = 3.0` → Tiempo inicial de avance recto (se recalcula aleatoriamente en cada ciclo). 
* `TURN_SPEED = 0.7` → Velocidad angular del robot. 
* `TURN_180_TIME = π / TURN_SPEED * random(0.7–1.3)` → Tiempo necesario para girar 180° con un factor aleatorio. 
* `INC_FACTOR = 0.0001` → Factor de incremento gradual de velocidad en el movimiento en espiral. 

---

## Lógica de Prioridad

El bumper tiene prioridad absoluta.
Si el robot detecta un choque:

1. Interrumpe cualquier estado en curso.
2. Cambia inmediatamente al **estado de giro 180° (2)**.
3. Después avanza recto (estado 3) y vuelve a la espiral.

Esto garantiza que el robot no se quede atascado ni repita siempre la misma trayectoria.
Además, al girar 180 grados nos aseguramos que al ir hacia alante si choca el bumper lo detecte, cosa que si fuese hacía
atras no pasaría, asegurandonos así no perder la reactividad.

---
## Video corto demostración

<a href="https://drive.google.com/file/d/1kHfPza1fUvgygHTrDiIwXL82aY1b6ggA/view?usp=sharing">
  <img 
    width="1717" 
    height="837" 
    alt="Captura desde 2025-10-04 13-57-45" 
    src="https://github.com/user-attachments/assets/45d01a2e-8ee5-40f7-a3b6-adb0e205cfb1" 
    style="cursor: pointer;"
  />
</a>

## Posibles Mejoras

* Variar no solo el giro de 180°, sino también giros de otros ángulos (ej. 90° o 120°).
* Incorporar sensores adicionales (infrarrojos, ultrasonidos, láser) para evitar colisiones sin necesidad de contacto.
* Implementar mapeo del entorno para recordar zonas ya exploradas.
* Ajustar dinámicamente la espiral para cubrir áreas de manera más eficiente.
* Poner una velocidad máxima para evitar que llegue a velocidades demasiado altas.

---

## Conclusión

Este algoritmo permite que un robot simulado explore su entorno mediante un patrón de espiral creciente, evitando colisiones gracias a un giro de 180°, evitando perder la reactividad y añadiendo variabilidad con movimientos rectos aleatorios. 
Es una base sencilla pero efectiva para robots exploradores, aspiradores o de búsqueda en entornos controlados.

---

