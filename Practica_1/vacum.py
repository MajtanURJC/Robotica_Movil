Recuerda ahora este:
import WebGUI
import HAL
import Frequency
import time
import random

# Parámetros
V_FORWARD = 0.2      # velocidad hacia adelante   
FORWARD_TIME = 3.0      #tiempo de avance
TURN_SPEED = 0.7    #velocidad de giro     
INC_FACTOR = 0.0001    #factor de incremento


# Estados
# 1 = avanzar en espiral
# 2 = girar 180 grados
# 3 = avanzar un tiempo aleatorio

STATE = 1
state_start = time.time() 

while True:
    bumper = HAL.getBumperData().state

    if bumper == 1 and STATE != 2:
        STATE = 2
        TURN_180_TIME = (3.14) / TURN_SPEED * random.uniform(0.7,1.3)   
        #tiempo en girar 180 grados y 
        #multiplicamos para evitar el 
        #mismo camino todo el rato
        state_start = time.time()
        
        
    if STATE == 1:  # avanzar en espiral
        HAL.setV(V_FORWARD)
        HAL.setW(TURN_SPEED)
        V_FORWARD += INC_FACTOR

    elif STATE == 2:  #girar 180 grados
        HAL.setV(0.0)          # no avanzar
        HAL.setW(TURN_SPEED)    # girar continuamente
        if time.time() - state_start >= TURN_180_TIME:
            STATE = 3 
            FORWARD_TIME = random.uniform(2.0,6.0)
            state_start = time.time()
            V_FORWARD = 0.7


    elif STATE == 3:  # avanzar
        HAL.setW(0.0)
        HAL.setV(V_FORWARD)
        if time.time() - state_start >= FORWARD_TIME:
            STATE = 1
            V_FORWARD = 0.2
            
    Frequency.tick()

