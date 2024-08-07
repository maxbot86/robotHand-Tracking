# robotHand-Tracking / Mano Robótica Controlada por Gestos

Este proyecto demuestra cómo controlar una **mano robótica** imitando los movimientos de una mano humana capturados a través de una cámara web. El proyecto está desarrollado en Python, utilizando OpenCV y MediaPipe para el reconocimiento de gestos, y un NodeMCU para controlar la mano robótica a través de WebSocket.

## Características

- **Reconocimiento de Gestos**: Utiliza MediaPipe para detectar los puntos de referencia de la mano y calcular los ángulos de las articulaciones de los dedos.
- **Control de la Mano Robótica**: Envía los ángulos calculados a la mano robótica, que replica los movimientos.
- **Control Remoto**: Usa WebSocket para el control en tiempo real de la mano robótica.

## Requisitos

- Python 3.7+
- OpenCV
- MediaPipe
- NumPy
- NodeMCU
- Hardware personalizado de la mano robótica

## Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/maxbot86/robotHand-Tracking.git
   cd robotHand-Tracking

2. **Instalar Dependencias**:
  ```bash
  pip install opencv-python mediapipe numpy
  ```

3. **Configurar tu NodeMCU:**:

  Asegúrate de que tu NodeMCU esté conectado a la misma red que tu computadora.
  Actualiza la dirección IP y el puerto en la instancia de robotHand en main.py para que coincidan con la configuración de tu NodeMCU.

4. **Ejecutar Script**:
  ```bash
  python main.py
  ```
