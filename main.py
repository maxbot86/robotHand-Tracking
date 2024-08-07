import cv2
import mediapipe as mp
import numpy as np
from robotHand import *


mcp_angle_prev = 0
dip_angle_prev = 0
pip_angle_prev = 0

# Defino un array de los dedos a controlar
fingers_arr = range(1,6)

#Defino una funcion para calcular el angulo de flexion con los 3 nodos de cada dedo
def calculate_angle(a, b, c):
    """
    Calcula el ángulo en el punto b formado por las líneas ab y bc.
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    ba = a - b
    bc = c - b
    try:
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)
    except:
        angle = 180
    
    return np.degrees(angle)

# Instanciamos la Mano Robotica
mano = robotHand('10.200.0.26',80)
#Mostramos si la URL de consulta es la correcta
mano.uri()
# Ponemos a Zero la posicion de los dedos.
mano.setZeroPos()

# Inicializar MediaPipe Hands.
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Configuración de la cámara.
cap = cv2.VideoCapture(0)

# Le damos contecto a la deteccion de la manos
# Uno de los datos claves es la cantidad de manos a detectar
# Si tuviesemos mas manos a instancia a distancia, podriamos dar para que detecte mas
with mp_hands.Hands(max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("No se pudo acceder a la cámara.")
            break

        # Convertir la imagen de BGR a RGB.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Procesar la imagen.
        results = hands.process(image)

        # Convertir de nuevo a BGR para OpenCV.
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Dibujar puntos de referencia y conexiones.
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Obtener las coordenadas de los puntos clave.
                landmarks = hand_landmarks.landmark
                # Convertir coordenadas normalizadas a píxeles.
                h, w, c = image.shape
                landmarks_pixel = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
                
                # Array para almacenar el grado de flexión de cada falange.
                finger_flexions = []

                # Detección del grado de flexión por cada dedo.
                for i in range(0, 5):
                    # Puntos clave para el dedo i.
                    base = landmarks_pixel[mp_hands.HandLandmark.WRIST + 4 * i]
                    mcp = landmarks_pixel[mp_hands.HandLandmark.THUMB_CMC + 4 * i]
                    pip = landmarks_pixel[mp_hands.HandLandmark.THUMB_MCP + 4 * i]
                    dip = landmarks_pixel[mp_hands.HandLandmark.THUMB_IP + 4 * i]
                    tip = landmarks_pixel[mp_hands.HandLandmark.THUMB_TIP + 4 * i]

                    # Calcular ángulos de las falanges.
                    try:
                        mcp_angle = round(calculate_angle(base, mcp, pip))
                        mcp_angle_prev = mcp_angle
                    except:
                        mcp_angle = mcp_angle_prev

                    try:
                        pip_angle = round(calculate_angle(mcp, pip, dip))
                        pip_angle_prev = pip_angle
                    except:
                        pip_angle = pip_angle_prev

                    try:
                        dip_angle = round(calculate_angle(pip, dip, tip))
                        dip_angle_prev = dip_angle
                    except:
                        dip_angle = dip_angle_prev

                    # Almacenar los ángulos en el array.
                    # Solo utilizo la falange mas alta por que en la mano robotica solo tengo una de control.
                    try:
                        if pip_angle > 180:
                            pip_angle=180
                        elif pip_angle<0:
                            pip_angle=0
                        else:
                            pass

                        try:
                            #En este punto invierto el angulo del flexion con respecto al angulo del servo
                            #Luego lo almaceno en el array
                            finger_flexions.append(180-pip_angle)
                        except:
                            finger_flexions.append(0)
                    except:
                        pass

                # Imprimir los grados de flexión solo para DEBUG.
                print(finger_flexions)
                
                #Luego de recorrer los 5 dedos hago el envio de la posicion de los dedos.
                mano.setEachPos(finger_flexions,fingers_arr)
        # Mostrar la imagen.
        cv2.imshow('Robotic Hand Tracking', image)
        if cv2.waitKey(5) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()