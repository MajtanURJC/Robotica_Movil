# Robotica_Movil


# Práctica 1

Este proyecto implementa un algoritmo de exploración autónoma para un robot simulado.
El robot combina un movimiento en espiral creciente con rutinas de evasión cuando detecta colisiones mediante su sensor bumper.

La lógica está programada en Python usando los módulos `WebGUI`, `HAL` y `Frequency`.

---

## Descripción del Comportamiento

El robot sigue un ciclo de cuatro estados principales:

1. **Avanzar en espiral (State 1)**

   * El robot avanza hacia adelante mientras describe una espiral creciente.
   * La velocidad lineal (`V_FORWARD`) aumenta poco a poco con cada ciclo gracias a `INC_FACTOR`.
   * La velocidad angular (`SPIRAL_SPEED`) genera el efecto de espiral.

2. **Retroceder (State 2)**

   * Si el bumper detecta un choque, el robot retrocede durante un tiempo fijo (`BACK_TIME`).
   * Esto evita quedarse atascado en el obstáculo.

3. **Girar a la izquierda (State 3)**

   * Después de retroceder, el robot gira sobre su eje hacia la izquierda (`TURN_SPEED`) durante un tiempo fijo (`TURN_TIME`).
   * Esto le da una nueva dirección antes de reanudar el movimiento.

4. **Avanzar recto (State 4)**

   * Para dar más variabilidad al recorrido, el robot avanza recto durante un tiempo aleatorio entre 1 y 3 segundos.
   * Tras esto, vuelve al movimiento en espiral.

El ciclo se repite indefinidamente.

---

## Parámetros principales

* `V_FORWARD = 0.4` → Velocidad inicial hacia adelante.
* `V_BACK = -0.4` → Velocidad al retroceder.
* `BACK_TIME = 1.0` → Tiempo de retroceso tras choque.
* `TURN_SPEED = 0.6` → Velocidad angular al girar.
* `TURN_TIME = 1.2` → Tiempo fijo de giro tras choque.
* `SPIRAL_SPEED = 0.6` → Velocidad angular usada en el movimiento en espiral.
* `INC_FACTOR = 0.0001` → Factor de incremento gradual de velocidad en espiral.

---

## Lógica de Prioridad

El bumper siempre tiene prioridad absoluta.
Si el robot detecta un choque:

1. Interrumpe cualquier estado en curso.
2. Cambia inmediatamente a **estado de retroceso (2)**.
3. Solo después continúa con el ciclo de evasión.

Esto garantiza que el robot nunca siga avanzando mientras está colisionando.

---

## Posibles Mejoras

* Ajustar dinámicamente `TURN_TIME` según el ángulo de impacto.
* Usar otros sensores (infrarrojo, láser) para evitar obstáculos sin necesidad de chocar.
* Implementar un mapeo del entorno para recordar zonas exploradas.
* Variar la espiral para cubrir el área más eficientemente.

---

## Conclusión

Este algoritmo permite que un robot se mueva de forma autónoma, explore áreas mediante un patrón de espiral creciente y evite quedar atascado gracias a una estrategia simple de evasión basada en el bumper.

Es una base ideal para robots aspiradores, exploradores o de búsqueda en entornos controlados.

---
