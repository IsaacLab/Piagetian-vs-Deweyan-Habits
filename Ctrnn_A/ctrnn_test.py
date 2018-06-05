import matplotlib.pyplot as plt
from pyeasyga import pyeasyga
from random import randint

import random
import math

# Sigmoid function
def sigmoid_math(x):
  return 1 / (1 + math.exp(-x))

# Plasticity check, as used in "On Adapation via Ultrastability", Candiate Number: 52804
def plasticity(max, min, y, b):
    activity = y + b
    p = 0.0
    if (activity < -max):
        p = -1
    elif (activity > max):
        p = 1
    elif (activity < -min):
        p = (0.5 * activity) + 1
    elif (activity > min):
        p = (0.5 * activity) - 1

    return p

# Angle normalization function
def normalize(angulo):
    a = angulo
    while (a > math.pi):
        a -= math.pi

    while (a < (-1 * math.pi)):
        a += math.pi

    return a

# Function that return the distance between two 2D points
def distance(x1,y1,x2,y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    # return math.hypot(x2 - x1, y2 - y1)

# GLOBAL VARIABLES
RADIO_AGENTE = 4    # Agent radius
DIAMETRO_AGENTE = RADIO_AGENTE * 2  # Agent diameter
DISTANCIA_LUZ_MIN = 20  # Min. distance that the lightsource can appear from the (0,0)
DISTANCIA_LUZ_MAX = 40  # Max. distance that the lightsource can appear from the (0,0)
DISTANCIA_MIN_FITNESS = RADIO_AGENTE * 4    # Distance in wich we consider the agent close enough to the lightsource
INTENSIDAD_LUZ_MIN = 500 # Min. value of light intensity
INTENSIDAD_LUZ_MAX = 1500 # Max. value of light intensity
SEPARACIONSENSOR = 1.0472 # Separation between sensor position and agent axis angle, 60º
VISIONSENSOR = 1.39626 # Reading arc of the sensor in wich it reads light inputs, 80
TIME_STEP = 0.2 # Integration time-step
N_INTERMEDIAS = 4
N_NEURONAS = N_INTERMEDIAS + 4
T = 800 # Variable to calculate the time the lightsource will be on

W_MAX = 10.0
W_MIN = -10.0
TAU_MAX = 4.0
TAU_MIN = 0.4
BIAS_MAX = 3.06
BIAS_MIN = -3.0
GAIN_MIN = 0.01
GAIN_MAX = 10.0

PLASTICIY_RATE_MAX = 0.9
PLASTICIY_RATE_MIN = -0.9

#Paste here the values returned by the file ctrnn.py at the end of the execution

individual = [[3.3777, 2.875, 0.8215, 1.9593, 1.7951, 2.8695, 2.9012, 1.4045], [1.2515, 1.2515, 9.7311, 9.7311], [-1.2793, 0.7352, -1.2363, -2.1884, 0.8226, -2.9676, 0.0904, -0.6806], [[-10.0, -10.0, -10.0, -10.0, -9.999999999999938, -5.893661984721517, -10.0, 10.0], [-9.999999999999998, -10.0, -10.0, -10.0, -9.987211637407636, 10.0, 10.0, 10.0], [10.0, -10.0, -9.997582244986877, 10.0, -10.0, 10.0, -10.0, 10.0], [-9.999999999999998, 10.0, -9.999999999999945, 10.0, -9.95921425517419, 9.999977520647471, 10.0, -9.999999999999998], [-10.0, 10.0, 10.0, -10.0, -10.0, -10.0, -10.0, 9.842095435320108], [10.0, 10.0, 10.0, -10.0, -10.0, -10.0, -9.999999999998737, -9.999065096389806], [10.0, -10.0, 10.0, 10.0, 10.0, -10.0, -9.999999999784196, 10.0], [-9.999999999999998, -9.999999999999996, 10.0, 10.0, 10.0, 9.999999999999998, -10.0, -10.0]], [[0.4917, -0.5191, 0.8173, -0.8557, -0.1377, -0.4108, 0.4628, -0.3924], [-0.1139, 0.3871, -0.855, 0.7382, -0.1407, -0.2975, -0.4983, -0.4347], [0.1136, 0.3332, -0.1262, 0.1614, 0.7148, 0.6144, 0.5525, -0.2395], [-0.3714, 0.769, 0.6703, -0.7626, -0.2461, 0.7142, 0.1955, -0.3529], [0.4467, 0.1894, 0.738, 0.4795, -0.3626, 0.2132, -0.294, 0.0856], [-0.2176, -0.3427, -0.1813, 0.0649, -0.6254, 0.3695, 0.076, -0.3286], [0.6934, -0.8399, 0.369, -0.2969, -0.0222, 0.0306, 0.6587, -0.6437], [-0.3324, -0.2086, 0.2182, 0.7907, 0.4249, 0.8665, -0.4357, -0.6617]], [3, 2, 0, 3, 0, 1, 3, 1]]

if __name__ == "__main__":
    # Agent starts at (0,0) and with a random orientation
    xAgente = 0.0
    yAgente = 0.0
    anguloAgente = random.random() * (2 * math.pi)

    # Inputs of the neurons
    inputs = []

    # Outputs of the neurons
    outputs = []

    for i in range(0, N_NEURONAS):
        outputs.append(0.0)
        inputs.append(0.0)

    # Creation of the lights that will participate in the experiment
    lucesX = []
    lucesY = []
    for i in range(0,6):

        angulo = random.random() * (2 * math.pi)
        distancia = round(random.uniform(DISTANCIA_LUZ_MIN, DISTANCIA_LUZ_MAX),2)
        lucesX.append(xAgente + (math.cos(angulo) * distancia)) # Light X position
        lucesY.append(yAgente + (math.sin(angulo) * distancia)) # Light Y position

## BEGINING OF THE EXPERIMENT
    historialX = []
    historialY = []
    endAgenteX = []
    endAgenteY = []

    for luces in range(0,6):
        xLuz = lucesX[luces]
        yLuz = lucesY[luces]
        intensidadLuz = random.randint(INTENSIDAD_LUZ_MIN, INTENSIDAD_LUZ_MAX)
        tiempoEncendida = random.randint(0.25 * T, 0.75 * T)   # Time the light will be on

        for ciclos in range(0, tiempoEncendida):
            inputs[0] = 0.0
            inputs[1] = 0.0

            # Angle between light and agent
            angAgenteLuz = normalize(math.atan2(yLuz - yAgente, xLuz - xAgente) - anguloAgente)

            # Sensor 1 vision limits
            llimit1 = normalize(SEPARACIONSENSOR + VISIONSENSOR)   # 60º + 80º in radians
            hlimit1 = normalize(SEPARACIONSENSOR - VISIONSENSOR)   # 60º - 80º in radians

            # Sensor 2 vision limits
            llimit2 = normalize(-SEPARACIONSENSOR + VISIONSENSOR)  # -60º + 80º in radians
            hlimit2 = normalize(-SEPARACIONSENSOR - VISIONSENSOR)  # -60º - 80º in radians

        # SENSOR UPDATE
            # First we check if the sensor are active
            s1Active = False
            s2Active = False

            if (angAgenteLuz <= llimit1):
                s1Active = True
                if (angAgenteLuz <= llimit2):
                    s2Active = True
            elif (angAgenteLuz >= hlimit2):
                s2Active = True
                if (angAgenteLuz >= hlimit1):
                    s1Active = True

            # If they are active we calculate they input
            if (s1Active == True):
                rad = normalize(anguloAgente + SEPARACIONSENSOR)
                xSensor1 = xAgente + ((RADIO_AGENTE) * math.cos(rad))
                ySensor1 = yAgente + ((RADIO_AGENTE) * math.sin(rad))

                # Square of the distance between the light and the sensor
                ds1 = distance(xSensor1, ySensor1, xLuz, yLuz)**2

                # Distance between the light and the center of the agent
                da = distance(xAgente, yAgente, xLuz, yLuz)

                a = (((RADIO_AGENTE) * (RADIO_AGENTE)) + ds1) / (da * da)

                if (a <= 1.0):
                    inputs[0] = intensidadLuz / ds1


            if (s2Active == True):
                rad = normalize(anguloAgente - SEPARACIONSENSOR)
                xSensor2 = xAgente + ((RADIO_AGENTE) * math.cos(rad))
                ySensor2 = yAgente + ((RADIO_AGENTE) * math.sin(rad))

                # Square of the distance between the light and the sensor
                ds2 = distance(xSensor2, ySensor2, xLuz, yLuz)**2

                # Distance between the light and the center of the agent
                da = distance(xAgente, yAgente, xLuz, yLuz)

                a = (((RADIO_AGENTE) * (RADIO_AGENTE)) + ds2) / (da * da)

                if (a <= 1.0):
                    inputs[1] = intensidadLuz / ds2

            # Multiply the input for the gain of the sensors
            inputs[0] = inputs[0] * math.exp(individual[1][0])
            inputs[1] = inputs[1] * math.exp(individual[1][1])

            # Make one run of the CTRNN function as used in "On Adapation via Ultrastability", Candiate Number: 52804
            for i in range(0, N_NEURONAS):
                change = -1.0 * outputs[i]

                for j in range(0, N_NEURONAS):
                    temp = outputs[j] + individual[2][j]
                    change += individual[3][j][i] * sigmoid_math(temp)

                # Read neuron input
                change +=inputs[i]

                # Tau factor application
                change = change / individual[0][i]

                # Save changes
                outputs[i] = outputs[i] + (change * TIME_STEP)

            # Update (or not) of the plasticity of the neurons depending on their plasticity type
            for i in range(0, N_NEURONAS):
                for j in range(0, N_NEURONAS):
                    if individual[5][j] != 0:   # If there is no plasticity, nothing is done
                        weight = individual[3][i][j]
                        jY = outputs[j]
                        jBias = individual[2][j]
                        iN = individual[4][i][j]
                        iRate = sigmoid_math(outputs[i] + individual[2][i])
                        jRate = sigmoid_math(outputs[j] + individual[2][j])

                        jPlastic = plasticity(4.0, 2.0, jY, jBias)

                        delta = 0.0

                        damping = W_MAX - math.fabs(weight)

                        if (individual[5][j] == 1):
                            delta = damping * iN * jPlastic * iRate * jRate
                        elif (individual[5][j] == 2):
                            threshold = (weight + W_MAX) * (W_MAX * 2)
                            delta = damping * iN * jPlastic * (iRate - threshold) * jRate
                        elif (individual[5][j] == 3):
                            threshold = (weight + W_MAX) / (W_MAX * 2)
                            delta = damping * iN * jPlastic * iRate * (jRate - threshold)

                        # Weight update
                        weight = weight + delta;
                        if (weight < W_MIN):
                            weight = W_MIN
                        elif (weight > W_MAX):
                            weight = W_MAX

                        # Save update weight
                        individual[3][i][j] = weight

            # UPDATE OF MOTOR VALUES AND AGENT POSITION
            vl = sigmoid_math(outputs[N_NEURONAS - 1] + individual[2][N_NEURONAS - 1])
            vr = sigmoid_math(outputs[N_NEURONAS - 2] + individual[2][N_NEURONAS - 2])

            # Value mapping between -1 and 1
            vl = (vl * 2.0) - 1.0
            vr = (vr * 2.0) - 1.0

            # Multiply the motor power for the gain of the motors
            vl = vl * individual[1][3]
            vr = vr * individual[1][2]

            v = (vl + vr) / 2.0
            w = (vr - vl) / (2.0 * RADIO_AGENTE)

            # Recalculate agent position
            xAgente += v * math.cos(anguloAgente) * TIME_STEP
            yAgente += v * math.sin(anguloAgente) * TIME_STEP

            historialX.append(xAgente)
            historialY.append(yAgente)

            # Update agent angle
            anguloAgente += normalize(w * TIME_STEP)

        # Agent coords at the end of the run for that lightsource
        endAgenteX.append(xAgente)
        endAgenteY.append(yAgente)


    plt.scatter(lucesX, lucesY, s=60, c='red', marker='^')
    plt.scatter(endAgenteX, endAgenteY, s=30, c='blue', marker='o')
    for i in range(0, len(lucesX)):
        plt.annotate(i, (lucesX[i],lucesY[i]))
        plt.annotate(i, (endAgenteX[i],endAgenteY[i]))
    plt.plot(historialX[0], historialY[0], "bo")
    plt.plot(historialX, historialY)
    plt.show()
