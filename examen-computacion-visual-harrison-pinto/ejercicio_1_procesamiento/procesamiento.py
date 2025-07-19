from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import torch

# 1. Cargar la imagen
img_path = Path('images/image.jpg')
img = cv2.imread(img_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 2. Suavizado Gaussiano
img_blur = cv2.GaussianBlur(img, (7, 7), 0)
img_blur_rgb = cv2.cvtColor(img_blur, cv2.COLOR_BGR2RGB)

# 3. Detección de bordes (Canny)
img_edges = cv2.Canny(img_blur, 100, 200)

# 4. Visualizar las tres etapas
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.imshow(img_rgb)
plt.title('Original')
plt.axis('off')
plt.subplot(1, 3, 2)
plt.imshow(img_blur_rgb)
plt.title('Suavizado (Gaussiano)')
plt.axis('off')
plt.subplot(1, 3, 3)
plt.imshow(img_edges, cmap='gray')
plt.title('Bordes (Canny)')
plt.axis('off')
plt.tight_layout()
plt.show()

# Crear carpeta de resultados si no existe
resultados_dir = Path('resultados')
resultados_dir.mkdir(parents=True, exist_ok=True)

# Guardar imagen suavizada
cv2.imwrite(resultados_dir / 'suavizado.png', img_blur)
# Guardar imagen de bordes
cv2.imwrite(resultados_dir / 'bordes.png', img_edges)

# 5. Detección de objetos con YOLOv5 (requiere torch y yolov5 instalados)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
results = model(img_rgb)

# 6. Mostrar imagen con bounding boxes y etiquetas
results.show()
