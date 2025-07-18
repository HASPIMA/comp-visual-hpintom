# Informe Taller Práctico 3 – Mundo estilo Minecraft con Three.js

## Objetivo

Crear un entorno 3D tipo Minecraft utilizando Three.js, geometría básica, texturas PBR, y elementos generados proceduralmente como terreno, árboles y criaturas.

---

## Descripción del Mundo

El mundo generado es un entorno de 10x10 bloques tipo voxel. Incluye un terreno generado proceduralmente con alturas controladas para mayor uniformidad visual. Sobre el terreno se distribuyen árboles y criaturas decorativas simples que le dan vida a la escena.

---

## Elementos Implementados

### Terreno tipo voxel
- Generado con `BoxGeometry`.
- Alturas controladas con ligeras variaciones (1-3 bloques).
- Guardado de mapa de alturas para posicionamiento.

###  Materiales PBR
- Texturas de pasto aplicadas: `albedo`, `normalMap`, `roughnessMap` y `aoMap`.
- Material generado con `MeshStandardMaterial`.
- Texturas repetidas correctamente para cubrir el terreno.

### Árboles procedurales
- Compuestos por tronco (`CylinderGeometry`) y hojas (`ConeGeometry`).
- Generados automáticamente en posiciones aleatorias y sobre el terreno.

### Criaturas decorativas
- Cuerpo cúbico con ojos esféricos.
- Colores predefinidos (rosado, azul, amarillo, rojo) y aleatorios si hay más.
- Rotación aleatoria para mayor naturalidad.

### Iluminación básica
- `AmbientLight` para iluminación suave global.
- `DirectionalLight` simulando la luz solar.

###  Cámara y navegación
- Cámara con `PerspectiveCamera`.
- Control orbital (`OrbitControls`) para explorar el mundo libremente.

---

##  Organización del Proyecto

```bash
src/
├── main.js           # lógica principal
├── terreno.js        # generación procedural del terreno
├── entidades.js      # árboles y criaturas
├── luces.js          # configuración de luces
└── textures/
    └── grass/        # texturas PBR del terreno
```

---

##  Ejemplo de material PBR aplicado

```js
const grassMaterial = new THREE.MeshStandardMaterial({
  map: albedo,
  normalMap: normal,
  roughnessMap: roughness,
  aoMap: ao
});
```

---

##  Reflexión Final

Este proyecto permitió explorar la creación de mundos procedurales combinando geometría básica, texturas PBR y agrupación de elementos. La separación en módulos facilitó la organización del código. Agregar criaturas con expresividad básica y rotación aleatoria dio un toque de personalidad al entorno.

---

##  Capturas

![alt text](<renders/Captura de pantalla 2025-07-05 013352.png>)
![alt text](<renders/Captura de pantalla 2025-07-05 013508.png>)
![alt text](<renders/Captura de pantalla 2025-07-05 013532.png>)

##  Enlace al proyecto 

https://codesandbox.io/p/sandbox/three-js-forked-944tt2
