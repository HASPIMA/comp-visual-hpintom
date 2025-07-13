# Taller - Realidad Aumentada con Marcadores usando AR.js

## 📅 Fecha
2025-07-12

---

## 🎯 Objetivo del Taller

Implementar una experiencia básica de realidad aumentada basada en marcadores directamente en el navegador, usando AR.js y A-Frame. El objetivo era proyectar un modelo 3D sobre un marcador físico detectado por la cámara web, sin necesidad de instalar aplicaciones externas.

---

## 🧠 Conceptos Aplicados

- Transformaciones geométricas básicas (escala, rotación, posición).
- Proyección de modelos 3D en realidad aumentada.
- Interacción con marcadores físicos (tipo "hiro").
- Integración de librerías WebXR como A-Frame y AR.js.

---

## 🔧 Herramientas y Entornos

- A-Frame v1.3.0
- AR.js v3.4.2 (desde `raw.githack.com`)
- Navegador moderno con acceso a cámara (Chrome)
- Live-server como entorno de desarrollo local (`npx live-server`)
- Modelo `.glb` descargado desde repositorios abiertos

---

## 📁 Estructura del Proyecto

```
2025-07-12_taller_arjs_marcadores/
├── index.html
├── models/
│   └── modelo.glb
├── markers/
│   └── hiro.png
├── README.md
```

---

## 🧪 Implementación

### 🔹 Etapas realizadas

1. Configuración del entorno local con `live-server` para evitar errores de seguridad por acceso a la cámara.
2. Uso de A-Frame con el componente de AR.js desde una fuente funcional (`raw.githack.com`) para evitar errores de tipo MIME que impedían la ejecución del script.
3. Inclusión del marcador tipo `hiro`, ya predefinido en AR.js.
4. Proyección de un modelo 3D en formato `.glb` sobre el marcador y animación básica de rotación.
5. Prueba de funcionamiento con cámara web y ajustes de escala/posición.

### 🔹 Código relevante

```html
<a-scene embedded arjs="sourceType: webcam;">
  <a-marker preset="hiro">
    <a-entity
      gltf-model="url(models/modelo.glb)"
      scale="1 1 1"
      position="0 0 0"
      animation="property: rotation; to: 0 360 0; loop: true; dur: 4000"
    ></a-entity>
  </a-marker>
  <a-entity camera></a-entity>
</a-scene>
```

---

## 📊 Resultados Visuales

> GIF incluido que muestra la detección del marcador y la proyección animada del modelo 3D.

![arjs_modelo_glb_detectado](./resultados/arjs_modelo_glb_detectado.gif)

---

## 🧩 Prompts o Búsqueda Utilizada

No se utilizaron prompts de IA para generación de imágenes. Sin embargo, se exploraron múltiples repositorios para encontrar un modelo `.glb` compatible con AR.js y A-Frame.

---

## 💬 Reflexión Final

Durante el desarrollo del taller se presentaron varias dificultades técnicas. Uno de los mayores retos fue encontrar una versión funcional y actualizada de la librería AR.js, ya que muchas fuentes disponibles en línea estaban desactualizadas o bloqueadas por los navegadores por problemas de tipo MIME. Después de probar con varios CDNs fallidos, se optó por `raw.githack.com`, que resolvió el problema.

Otra dificultad fue conseguir un modelo `.glb` adecuado. Muchos repositorios exigían registrarse o no permitían la descarga libre. Algunos modelos descargados no cargaban correctamente o estaban dañados. Finalmente, se logró incluir uno funcional con animación de rotación.

Este taller permitió reforzar el conocimiento sobre integración de tecnologías web modernas para experiencias de realidad aumentada, y evidenció las limitaciones prácticas al trabajar con recursos externos y bibliotecas no centralizadas.

---

## ✅ Checklist de Entrega

- [x] Carpeta con estructura solicitada
- [x] Código funcional (`index.html`)
- [x] GIF mostrando la proyección AR
- [x] Modelo `.glb` en carpeta `/models/`
- [x] README completo con reflexión final
