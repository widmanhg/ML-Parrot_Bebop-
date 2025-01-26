from pyparrot.Bebop import Bebop
from pyparrot.DroneVision import DroneVision
from pyparrot.Model import Model
import cv2
import torch
from ultralytics import YOLO

# Inicializa el modelo YOLO
model = YOLO('best.pt')

# Parámetros de optimización
process_frame_interval = 10  # Procesar cada 10 fotogramas
frame_count = 0

# Función para mover el dron basado en la posición del centroide
def move_drone_based_on_centroid(centroid_x, centroid_y, width, height):
    if centroid_x > width // 2 + 30:
        print("Moviendo a la derecha")
        bebop.fly_direct(roll=15, pitch=0, yaw=0, vertical_movement=0, duration=1)
    elif centroid_x < width // 2 - 30:
        print("Moviendo a la izquierda")
        bebop.fly_direct(roll=-15, pitch=0, yaw=0, vertical_movement=0, duration=1)
    else:
        print("Centrado horizontalmente")

    if centroid_y < height // 2 - 30:
        print("Subiendo")
        bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=15, duration=1)
    elif centroid_y > height // 2 + 30:
        print("Bajando")
        bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-15, duration=1)
    else:
        print("Centrado verticalmente")

    # Si está centrado horizontal y verticalmente, avanzar hacia el objeto
    if abs(centroid_x - width // 2) < 30 and abs(centroid_y - height // 2) < 30:
        print("Avanzando para atravesar la ventana")
        bebop.fly_direct(roll=0, pitch=50, yaw=0, vertical_movement=0, duration=2)

# Función de callback para mostrar el video y aplicar YOLO
def display_video_frame(args):
    global frame_count
    img = bebopVision.get_latest_valid_picture()
    if img is not None:
        frame_count += 1
        
        # Procesar cada n-ésimo fotograma
        if frame_count % process_frame_interval == 0:
            # Reducción de la resolución de la imagen
            img_small = cv2.resize(img, (640, 480))  # Ajusta la resolución según sea necesario

            # Aplica el modelo YOLO en la imagen capturada del dron
            results = model(img_small)

            # Renderiza las detecciones en la imagen
            annotated_img = results[0].plot()

            # Extraer las coordenadas de las detecciones
            for result in results[0].boxes.xyxy:  # x1, y1, x2, y2
                x1, y1, x2, y2 = map(int, result)
                # Calcular el centro del objeto
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                # Dibujar el centro del objeto en la imagen
                cv2.circle(annotated_img, (center_x, center_y), 5, (0, 255, 0), -1)  # Círculo verde

                # Mover el dron basado en la posición del centroide
                move_drone_based_on_centroid(center_x, center_y, 640, 480)

            # Muestra el video con las detecciones YOLO
            cv2.imshow("Bebop Video Feed with YOLO", annotated_img)

        # Salir del bucle si se presiona 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            bebopVision.close_video()
            bebop.disconnect()
            cv2.destroyAllWindows()
            return False
    return True

# Crear objeto Bebop
bebop = Bebop()

# Conectar al Bebop
success = bebop.connect(5)

if success:
    # Realiza el despegue seguro
    bebop.safe_takeoff(timeout=10)  # Timeout de 10 segundos
    
    # Configurar la visión del dron
    bebopVision = DroneVision(bebop, Model.BEBOP)
    
    # Configurar la función de callback
    bebopVision.set_user_callback_function(display_video_frame, user_callback_args=None)
    
    # Iniciar la transmisión de video
    success = bebopVision.open_video()

    if success:
        print("Transmisión de video iniciada con éxito.")
        print("Presiona 'q' para cerrar la ventana de video.")
        
        # Mantener la ventana abierta hasta que se presione 'q'
        while True:
            bebop.smart_sleep(1)  # Mantener el hilo vivo y permitir que se actualicen los frames
    else:
        print("No se pudo iniciar la transmisión de video.")
    
    # Desconectar el drone (esto no se alcanzará a menos que se presione 'q')
    bebop.disconnect()
else:
    print("Error al conectar con el Bebop. Intenta nuevamente.")
