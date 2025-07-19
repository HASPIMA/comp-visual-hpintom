import cv2
from ultralytics import YOLO
import pandas as pd
from datetime import datetime
import os

# ========================
# CONFIGURACIÓN
# ========================

VIDEO_PATH = "videos/videoSeguridad.mp4"
CAPTURAS_DIR = "../capturas"
LOGS_DIR = "../logs"
LOG_FILE = os.path.join(LOGS_DIR, "eventos.csv")

# Crear carpetas
os.makedirs(CAPTURAS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Crear log si no existe
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=["timestamp", "evento", "clase", "confianza"]).to_csv(LOG_FILE, index=False)

# Cargar modelo YOLOv8 (versión ligera)
model = YOLO("yolov8n.pt")  # Usa yolov8s.pt o yolov8m.pt si quieres más precisión

# ========================
# LECTURA DE VIDEO
# ========================

cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print(f"[ERROR] No se pudo abrir el video: {VIDEO_PATH}")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("[INFO] Fin del video.")
        break

    # Inferencia
    results = model(frame)[0]  # Primer frame del batch
    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        label = model.names[cls_id]

        if label == "person" and conf >= 0.6:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            filename = f"persona_{timestamp.replace(':', '-')}.jpg"
            filepath = os.path.join(CAPTURAS_DIR, filename)

            cv2.imwrite(filepath, frame)
            df = pd.DataFrame([[timestamp, "Persona detectada", label, round(conf, 2)]])
            df.to_csv(LOG_FILE, mode='a', header=False, index=False)

            print(f"[ALERTA] Persona detectada - Confianza: {round(conf, 2)}")

    # Mostrar frame con resultados
    annotated_frame = results.plot()
    resized = cv2.resize(annotated_frame, (960, 540))  # o (1280, 720)
    cv2.imshow("Sistema de Monitoreo - YOLOv8", resized)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
