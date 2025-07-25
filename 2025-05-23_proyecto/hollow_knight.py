# hollow_knight.py
import time
import cv2
import keyboard

class HollowKnightGame:
    def __init__(self):
        self.last_jump_time = 0
        self.jump_cooldown = 1.2  # evitar spam de saltos
        self.last_z_time = 0
        self.z_cooldown = 0.5

    def handle_pose_output(self, action):
        """
        Ejecuta una acción basada en el gesto detectado por pose_detector
        """
        if action == "left":
            keyboard.press("left")
            return True
        elif action == "right":
            keyboard.press("right")
            return True
        elif action == "release":
            keyboard.release("left")
            keyboard.release("right")
            return False
        elif action == "z":
            if time.time() - self.last_z_time > self.z_cooldown:
                keyboard.press_and_release("z")
                self.last_z_time = time.time()
                return True
        elif action == "x":
            if time.time() - self.last_jump_time > self.jump_cooldown:
                keyboard.press_and_release("x")
                self.last_jump_time = time.time()
                return True
        elif action == "menu":
            return "menu"
        return False

    def draw_info(self, frame):
        """
        Dibuja instrucciones del juego Hollow Knight sobre la pantalla
        """
        height, width = frame.shape[:2]
        overlay = frame.copy()
        cv2.rectangle(overlay, (50, 50), (width - 50, height - 50), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

        y = 100
        spacing = 35

        def put(text, color=(255, 255, 255)):
            nonlocal y
            cv2.putText(frame, text, (80, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            y += spacing

        put("HOLLOW KNIGHT (control corporal)", (0, 255, 255))
        put("Inclinar cuerpo a la izquierda:  ")
        put("Inclinar cuerpo a la derecha:    ")
        put("Levantar brazo:                  Z (disparo)")
        put("Tocarse ambas rodillas:          X (salto)")
        put("Postura recta y brazos abajo:    Volver al menú")
        return frame
