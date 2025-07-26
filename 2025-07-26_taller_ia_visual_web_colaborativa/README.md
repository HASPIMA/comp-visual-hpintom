# IA Visual Web Colaborativa - Taller

## 📌 ¿Qué se detectó?
Se aplicó YOLOv8 sobre varias imagenes de prueba. Se detectaron objetos con confianza mayor al 0.5.

## 🎯 Imagenes de Prueba
![imagen0](python/imagen0.jpg)
![imagen1](python/imagen1.jpg)
![imagen2](python/imagen2.jpg)
![imagen3](python/imagen3.jpg)
![imagen4](python/imagen4.jpg)

## 🎯 Imagenes resultado
![deteccion_0](web/resultados/deteccion_0.png)
![deteccion_1](web/resultados/deteccion_1.png)
![deteccion_2](web/resultados/deteccion_2.png)
![deteccion_3](web/resultados/deteccion_3.png)
![deteccion_4](web/resultados/deteccion_4.png)

## 🌐 Json resultado
![deteccion_0_json](web/resultados/deteccion_0.json)
![deteccion_1_json](web/resultados/deteccion_1.json)
![deteccion_2_json](web/resultados/deteccion_2.json)
![deteccion_3_json](web/resultados/deteccion_3.json)
![deteccion_4_json](web/resultados/deteccion_4.json)

## 🎥 Visualización Web
Página estática que carga:
- Las imagenes con detecciones.
- Datos en una tabla extraídos del JSON por cada imagen.

## 🧠 Reflexión
Este taller me permitió entender cómo representar visualmente los resultados de un modelo IA. Publicarlos en una página web ayuda a que otros los comprendan fácilmente. Fue un reto lograr que todos los archivos se comunicaran correctamente, pero el resultado es modular y puede adaptarse a otros modelos.