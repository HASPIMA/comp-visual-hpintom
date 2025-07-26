import cv2
import os
import json
from datetime import datetime
from ultralytics import YOLO

# Crear carpeta de salida
os.makedirs("../resultados", exist_ok=True)

# Cargar modelo YOLOv8
model = YOLO("yolov8n.pt")

# Lista de imágenes a procesar
imagenes = [
    "imagen0.jpg",
    "imagen1.jpg",
    "imagen2.jpg",
    "imagen3.jpg",
    "imagen4.jpg"
]

# Procesar cada imagen
for idx, nombre_img in enumerate(imagenes):
    img = cv2.imread(nombre_img)
    if img is None:
        print(f"⚠️ No se pudo leer {nombre_img}, se omite.")
        continue

    results = model(img)[0]
    detecciones = []

    for r in results.boxes:
        x1, y1, x2, y2 = r.xyxy[0].tolist()
        w, h = x2 - x1, y2 - y1
        clase = model.names[int(r.cls)]
        confianza = float(r.conf)

        detecciones.append({
            "class": clase,
            "confidence": confianza,
            "x": int(x1),
            "y": int(y1),
            "w": int(w),
            "h": int(h)
        })

    # Guardar imagen anotada
    salida_img = f"../web/resultados/deteccion_{idx}.png"
    cv2.imwrite(salida_img, results.plot())

    # Guardar archivo JSON
    salida_json = f"../web/resultados/deteccion_{idx}.json"
    json_data = {
        "timestamp": datetime.now().isoformat(),
        "image": nombre_img,
        "objects": detecciones
    }
    with open(salida_json, "w") as f:
        json.dump(json_data, f, indent=2)

    print(f"✅ Procesada {nombre_img} → {salida_img}, {salida_json}")

import csv

with open("../web/resultados/resumen.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["class", "confidence", "x", "y", "w", "h"])
    writer.writeheader()
    writer.writerows(detecciones)
