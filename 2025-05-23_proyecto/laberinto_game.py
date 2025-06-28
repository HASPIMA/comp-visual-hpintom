import cv2
import keyboard
import time

class LaberintoGame:
    def __init__(self):
        self.last_gesture_time = 0
        self.gesture_cooldown = 0.3  # segundos entre gestos

    def handle_gesture(self, gesture_type):
        """
        Ejecuta una acción en el juego según el gesto detectado.
        gesture_type: 'up', 'down', 'left', 'right'
        """
        current_time = time.time()
        if current_time - self.last_gesture_time < self.gesture_cooldown:
            return False

        key_mapping = {
            'up': 'up',
            'down': 'down',
            'left': 'left',
            'right': 'right',
        }

        if gesture_type in key_mapping:
            try:
                keyboard.press_and_release(key_mapping[gesture_type])
                self.last_gesture_time = current_time
                print(f"Laberinto: Tecla {key_mapping[gesture_type]} presionada")
                return True
            except Exception as e:
                print(f"Error simulando tecla: {e}")
        return False

    def draw_info(self, frame):
        """Muestra un overlay con instrucciones del juego del laberinto"""
        height, width = frame.shape[:2]
        margin_x = int(width * 0.1)
        margin_y = int(height * 0.1)

        overlay = frame.copy()
        cv2.rectangle(overlay, (margin_x, margin_y),
                      (width - margin_x, height - margin_y), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

        y = margin_y + 40
        spacing = 35

        def put(text, color=(255, 255, 255)):
            nonlocal y
            cv2.putText(frame, text, (margin_x + 30, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            y += spacing

        put("Indice arriba       → Mover ARRIBA ↑")
        put("Mano abierta         → Mover ABAJO ↓")
        put("Pulgar izquierda     → Mover IZQUIERDA ←")
        put("Pulgar derecha       → Mover DERECHA →")
        put("Signo paz (1.2s)     → Volver al menú")
        put("Signo rock (2s)      → Cerrar programa")

        return frame
