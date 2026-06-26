# Práctica – Navegación Global mediante descenso de gradiante con coche modelo ackerman

Este proyecto implementa un sistema de navegación global basado en el descenso de gradiante.
El objetivo es que el robot alcance el destino seleccionado en el mapa siguiendo el gradiente descendente del campo de potencial, mientras evita colisiones gracias a un inflado artificial de los obstáculos.

## Descripción del Comportamiento

El robot ejecuta un bucle de control continuo que sigue estos pasos:

### 1. **Carga del mapa y preprocesado**

* Se obtiene la imagen del mapa con:

  ```python
  array = WebGUI.getMap('/resources/exercises/global_navigation/images/cityLargenBin.png')
  array = (array > 127).astype(np.uint8)
  ```

* Las celdas con valor `0` representan edificios y las `1` zonas transitables.


### 2. **Selección del destino**

* El usuario marca un punto en el mapa mediante la interfaz gráfica (`WebGUI.getTargetPose()`).
* El destino se convierte a coordenadas de la rejilla usando `WebGUI.rowColumn()`.

Cuando el destino cambia, se recalcula el campo de potencial.

### 3. **Cálculo del Wave Front Algorithm**

El algoritmo se expande desde el destino hasta un poco más de la posición del coche, asignando valores crecientes a cada celda y 
a los valores cercanos a los obstaculos dandoles un valor muy alto para no bloquear pero intentar que el coche a no ser que 
sea imprescindible no pase por esa zona, lo que he definido como un inflado artificial:

```python
campo = wavefront_bfs(goal_r, goal_c, robot_r, robot_c, expandir_extra=15)
WebGUI.showNumpy(campo)
```

Características principales:

* La expansión se detiene cuando alcanza el robot + un margen configurable que yo he puesto de 15.
* Las celdas infladas reciben un valor muy alto para tratar de que no sean usadas pero tampoco bloquarlas.
* El resultado es un mapa de potencial con el cual se llegará hasta el objetivo.

Se hace siguiendo estos pasos del guión:

<img width="421" height="197" alt="image" src="https://github.com/user-attachments/assets/5bc0f9a3-655c-434b-834a-d506da0c3e10" />


### 4. **Selección del siguiente movimiento**

El robot busca, entre sus vecinos, aquellos cuya distancia potencial sea menor que la actual.
Para evitar ir mirando directamente "a nuestros pies", se evalúan 1, 2 y 3 celdas hacia adelante 
en la misma dirección antes de tomar una decisión.

Para decidir que vecino es el mejor se le aplica un valor cada movimiento, siendo 1 los vecinos directos
hacia arriba, abajo, derecha e izquierda, y siendo raiz de dos los movimientos diagonales.

Una vez se calculan los mejores vecinos con el gasto y con el valor se guardan para sacar el angulo
y poder llegar a ellos con el coche.


### 5. **Conversión a velocidades**

A partir del vector de dirección seleccionado (dx, dy), que representa el movimiento deseado en el plano del mapa, se obtiene primero el ángulo objetivo hacia el que el robot debe orientarse. Para ello se utiliza la función atan2, que permite calcular correctamente el ángulo en función de los signos de ambos componentes del vector.

Después, este ángulo objetivo se compara con la orientación actual del robot  para obtener el error angular, es decir, la desviación entre la dirección actual y la dirección deseada.

A partir de este error se generan las velocidades del robot:

- La velocidad angular se mantiene proporcional al error de orientación, de forma que el robot gira más rápido cuanto más desalineado está.
- La velocidad lineal ya no es constante, sino que depende del propio error angular.

Esto significa que el robot avanza a máxima velocidad cuando está bien orientado hacia el objetivo, pero reduce progresivamente su velocidad cuando necesita girar. Si el giro es muy grande, la velocidad se reduce casi a cero, permitiendo que el robot primero se reoriente antes de avanzar.

Mediante este comportamiento conseguimos que sea muy dificil que el coche se choque con paredes y que al tener que cambiar de dirección lo pueda hacer
de manera segura.

El coche siempre avanza hacia el punto de menor gradiente dentro del campo de potencial, es decir, el más oscuro visualmente.

### 6. **Detección de llegada al destino**

Cuando el robot está suficientemente cerca del objetivo, se detiene a la espera de que le mandes otra posición u otra orden, 
se puede configurar lo cerca que quieres que se quede del objetivo, en estre caso yo le he puesto 2 celdas de cercanía al objetivo
que se detenga, de este modo:

```python
if abs(robot_r - goal_r) <= 2:
    HAL.setV(0)
    HAL.setW(0)
```

## Inflado de Obstáculos

El inflado consiste en ampliar artificialmente las zonas ocupadas marcando con un valor muy alto para que en el momento
de que el coche vea el valor de los vecinos más cercanos decida no cogerlo y tratar de evitar esas zonas, yo he puesto un valor
de 60 siendo configurable en la llamada a la función.

Esto hace que al elegir el de menor potencial, nunca vaya a elegir esos muy inflados a no ser que sea vital para la ruta, evitando asi prohibirlos.


## Visualización

El campo generado por el algoritmo se muestra mediante la interfaz gráfica:

```python
WebGUI.showNumpy(campo)
```

La imagen resultante muestra como según te acercas a la posición objetivo las celdas van teniendo menos potencial y haciendose así más oscuras,
en cambio, cuanto más nos alejamos del objetivo, más potencial tiene y más blanco se ve.

## Video agregado

https://github.com/user-attachments/assets/ca8e2f1a-a0e6-4e23-add4-ed00e44aa3ac

## Video demostración de la expanosión:

https://github.com/user-attachments/assets/8c487456-535c-4b82-85bc-d242bf657749

Se puede ver en esta expansión que cuando clicamos en un callejon sin salida, los puntos con menor potencial son los del pasillo en cambio al otro lado del muro podemos ver que tiene mucho potencial a pesar de estar cerca. Esto es debido a que el campo de potencial solo se expande por areas libres y no se expande por areas con obstaculos o prohibidas.
