import time
import keyboard

class DinoGame:
    def __init__(self):
        self.last_jump_time = 0
        self.jump_cooldown = 0.3  # Cooldown entre saltos para evitar spam
        
    def handle_gesture(self, is_hand_open):
        """Maneja los gestos para el juego del dinosaurio"""
        current_time = time.time()
        
        if is_hand_open and (current_time - self.last_jump_time > self.jump_cooldown):
            keyboard.press('space')
            self.last_jump_time = current_time
            return True  # Indica que se realizó un salto
        
        return False
    
    def draw_info(self, frame):
        """Dibuja información del juego en el frame"""
        import cv2
        
        # Overlay para el estado del juego
        cv2.putText(frame, "MODO JUEGO DEL DINOSAURIO", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(frame, "Mano abierta: Saltar", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(frame, "Signo paz (1.2s): Volver al menu", (10, 85), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(frame, "Signo rock (2s): Cerrar programa", (10, 110), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        return frame
