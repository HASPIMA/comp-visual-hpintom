# 🎮 GESTIK - Sistema de Control por Gestos

## 📋 **Resumen del Proyecto**

**GESTIK** es un sistema interactivo de control por gestos que permite jugar videojuegos usando únicamente movimientos de manos y poses corporales, eliminando la necesidad de teclado o mouse. Utiliza visión por computadora en tiempo real para detectar gestos y traducirlos en comandos de juego.

---

## 🛠️ **Tecnologías Utilizadas**

### **Inteligencia Artificial y Visión por Computadora:**
- **MediaPipe** (v0.10.21+): Framework de Google para detección de manos y poses corporales
- **OpenCV** (v4.11.0+): Procesamiento de video y manipulación de imágenes
- **NumPy**: Cálculos matemáticos para análisis de landmarks

### **Interfaz y Presentación:**
- **tkinter**: GUI nativa de Python para ventana redimensionable con icono personalizado
- **PIL/Pillow**: Conversión y manipulación de imágenes para la interfaz

### **Control de Sistema:**
- **keyboard**: Simulación de teclas para controlar juegos externos
- **threading**: Manejo de temporizadores para gestos prolongados

### **Gestión de Proyecto:**
- **uv**: Gestor moderno de dependencias de Python
- **Python 3.11.9**: Lenguaje base con tipado y estructuras modernas

---

## ⚙️ **Flujo de Trabajo**

### **1. Captura y Procesamiento (Tiempo Real)**
```
Cámara → OpenCV → MediaPipe → Análisis de Landmarks → Detección de Gestos
```

### **2. Sistema de Estados**
```
MAIN_MENU ↔ DINO_GAME ↔ LABERINTO_GAME ↔ HOLLOW_KNIGHT
```

### **3. Pipeline de Detección**
1. **Captura de frame** (30 FPS objetivo)
2. **Procesamiento MediaPipe** (detección simultánea de manos y poses)
3. **Análisis de landmarks** (coordenadas 3D normalizadas)
4. **Clasificación de gestos** (lógica personalizada por juego)
5. **Ejecución de comandos** (simulación de teclas)

---

## 🎯 **Funcionalidades Principales**

### **Control Universal:**
- **Navegación de menú:** Gestos de mano para seleccionar juegos
- **Cambio de contexto:** Signo de paz (1.2s) para alternar menú/juego
- **Cierre seguro:** Signo de rock (2s) para terminar aplicación

### **Detección de Gestos de Mano:**
- **Pulgar arriba/abajo:** Navegación vertical en menús
- **Mano abierta:** Selección/confirmación y salto
- **Puño cerrado:** Estados de espera y detección de cambios
- **Meñique arriba:** Movimiento hacia la izquierda
- **Pulgar derecha:** Movimiento hacia la derecha (requiere más extensión)

### **Detección de Poses Corporales (Hollow Knight):**
- **Inclinación lateral:** Detección de movimiento derecha/izquierda
- **Posición de rodillas:** Activación de salto según separación
- **Sistema de estados:** Prevención de spam con lógica press/release

### **Adaptabilidad por Juego:**
- **Chrome Dino:** Control simple de salto
- **Laberinto:** Navegación direccional completa
- **Hollow Knight:** Control avanzado con poses corporales

---

## 🧠 **Arquitectura del Sistema**

### **Modularidad:**
- **`main.py`:** Coordinador principal y GUI
- **`gesture_detector.py`:** Lógica de detección de gestos de mano
- **`pose_detector.py`:** Análisis de poses corporales
- **`game_states.py`:** Enum de estados del sistema
- **`*_game.py`:** Módulos específicos por juego

### **Características Técnicas:**
- **Anti-flickering:** Tolerancias para evitar detecciones erróneas
- **Temporizadores:** Gestos prolongados para acciones críticas
- **Debug integrado:** Sistema de logging para desarrollo
- **Interfaz profesional:** Ventana redimensionable con icono personalizado

---

## 🎯 **Casos de Uso y Aplicaciones**

### **Gaming Accesible:**
- Personas con limitaciones de movilidad en manos
- Gaming inmersivo sin dispositivos físicos
- Ejercicio físico mientras se juega

### **Demostraciones Tecnológicas:**
- Pruebas de concepto de visión por computadora
- Interfaces naturales usuario-máquina
- Aplicaciones de MediaPipe en tiempo real

### **Educación e Investigación:**
- Enseñanza de computer vision
- Desarrollo de interfaces gestuales
- Análisis de precisión en detección de gestos

---

# 📊 **Estructura de Diapositivas Sugerida**

## **Diapositiva 1: Portada**
- **Título:** GESTIK - Control de Videojuegos por Gestos
- **Subtítulo:** Sistema de Visión por Computadora en Tiempo Real
- **Autores y fecha**

## **Diapositiva 2: Problema y Motivación**
- **Problema:** Limitaciones de controles tradicionales
- **Motivación:** Interfaces naturales y accesibilidad
- **Objetivo:** Gaming sin dispositivos físicos

## **Diapositiva 3: Tecnologías Clave**
- **MediaPipe:** Detección de manos y poses
- **OpenCV:** Procesamiento de video
- **Python:** Ecosistema de desarrollo
- **Arquitectura modular**

## **Diapositiva 4: Demostración en Vivo**
- **Video/GIF:** Navegación por menús con gestos
- **Casos:** Control de diferentes juegos
- **Destacar:** Fluidez y precisión

## **Diapositiva 5: Gestos Implementados**
- **Tabla visual:** Gesto → Acción
- **Imágenes:** Screenshots de gestos detectados
- **Diferenciación:** Por contexto de juego

## **Diapositiva 6: Arquitectura del Sistema**
- **Diagrama de flujo:** Cámara → Procesamiento → Control
- **Módulos:** Separación de responsabilidades
- **Estados:** Transiciones entre juegos

## **Diapositiva 7: Desafíos Técnicos**
- **Precisión:** Evitar falsos positivos/negativos
- **Rendimiento:** Procesamiento en tiempo real
- **Usabilidad:** Gestos intuitivos y naturales

## **Diapositiva 8: Resultados y Métricas**
- **Precisión:** 90-94% para gestos principales
- **Responsividad:** ~50ms tiempo de respuesta
- **Rendimiento:** Funcionamiento fluido en tiempo real
- *(Mencionar brevemente las métricas generadas)*

## **Diapositiva 9: Casos de Uso**
- **Accesibilidad:** Gaming inclusivo
- **Educación:** Aprendizaje de computer vision
- **Entretenimiento:** Gaming inmersivo

## **Diapositiva 10: Trabajo Futuro**
- **Más gestos:** Expansión del vocabulario gestual
- **Más juegos:** Integración con otros títulos
- **Optimización:** Mejoras de rendimiento
- **ML personalizado:** Adaptación por usuario

## **Diapositiva 11: Conclusiones**
- **Viabilidad:** Sistema funcional y estable
- **Impacto:** Nuevas formas de interacción
- **Aprendizajes:** Computer vision aplicada

## **Diapositiva 12: Demo y Preguntas**
- **Invitación:** Prueba del sistema
- **Contacto:** Información del equipo
- **Q&A:** Espacio para preguntas

---

## 💡 **Consejos para la Presentación:**

1. **Enfócate en la demostración:** El sistema funcionando vale más que mil palabras
2. **Explica los desafíos:** Detección en tiempo real es complejo
3. **Destaca la modularidad:** Fácil agregar nuevos juegos/gestos
4. **Menciona accesibilidad:** Impacto social del proyecto
5. **Prepara backup:** Videos en caso de problemas técnicos

¡El proyecto está muy completo y tiene gran potencial para una presentación impactante! 🚀
