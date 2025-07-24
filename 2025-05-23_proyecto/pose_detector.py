# pose_detector.py
import time
from mediapipe.python.solutions.pose import PoseLandmark

class PoseDetector:
    def __init__(self):
        self.last_pose = None
        self.last_pose_time = 0
        self.menu_hold_start = None
        self.menu_hold_duration = 3.0  # 3 segundos para palmas tocándose
        
        # Para tolerancia al flickering (similar a gesture_detector)
        self.gesture_tolerance_time = 0.2  # 200ms de tolerancia

    def are_palms_touching(self, left_wrist, right_wrist):
        """Detecta si las palmas de las manos están tocándose"""
        # Calcular la distancia entre las muñecas
        distance_x = abs(left_wrist.x - right_wrist.x)
        distance_y = abs(left_wrist.y - right_wrist.y)
        
        # Las palmas están tocándose si las muñecas están muy cerca
        # Umbral más generoso para permitir pequeñas variaciones
        distance_threshold = 0.08  # Ajustable según sea necesario
        
        # Verificar que ambas manos están en posición central (no extendidas)
        # y que están a una altura similar
        hands_close = (distance_x < distance_threshold and distance_y < distance_threshold)
        
        # Verificar que las manos están a una altura razonable (no muy arriba ni muy abajo)
        reasonable_height = (0.3 < left_wrist.y < 0.8 and 0.3 < right_wrist.y < 0.8)
        
        return hands_close and reasonable_height

    def detect_action(self, landmarks):
        current_time = time.time()

        left_shoulder = landmarks[PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[PoseLandmark.RIGHT_SHOULDER.value]
        nose = landmarks[PoseLandmark.NOSE.value]
        left_wrist = landmarks[PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[PoseLandmark.RIGHT_WRIST.value]
        left_elbow = landmarks[PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[PoseLandmark.RIGHT_ELBOW.value]
        left_knee = landmarks[PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[PoseLandmark.RIGHT_KNEE.value]

        torso_x = (left_shoulder.x + right_shoulder.x) / 2
        torso_y = (left_shoulder.y + right_shoulder.y) / 2

        # LEFT/RIGHT tilt
        if right_shoulder.x - left_shoulder.x > 0.16:
            return "left"
        elif left_shoulder.x - right_shoulder.x > 0.16:
            return "right"

        # JUMP (both hands near knees)
        hands_near_knees = (
            abs(left_wrist.y - left_knee.y) < 0.1 and
            abs(right_wrist.y - right_knee.y) < 0.1
        )
        if hands_near_knees:
            return "x"

        # Z: arm lifted above head
        if left_wrist.y < nose.y or right_wrist.y < nose.y:
            return "z"

        # MENU: palmas tocándose por 3 segundos (con tolerancia al flickering)
        if self.are_palms_touching(left_wrist, right_wrist):
            if self.menu_hold_start is None:
                self.menu_hold_start = current_time
                print("DEBUG: Iniciando contador palmas tocándose...")
            elif current_time - self.menu_hold_start > self.menu_hold_duration:
                print("DEBUG: Palmas tocándose mantenidas por 3 segundos - ir al menú")
                self.menu_hold_start = None  # Reset para evitar repetición
                return "menu"
            else:
                remaining = self.menu_hold_duration - (current_time - self.menu_hold_start)
                print(f"DEBUG: Palmas tocándose... {remaining:.1f}s restantes")
        else:
            # Solo resetear si han pasado algunos frames sin el gesto (tolerancia al flickering)
            if self.menu_hold_start is not None:
                # Dar una pequeña tolerancia de tiempo para el flickering
                time_since_start = current_time - self.menu_hold_start
                if time_since_start < self.gesture_tolerance_time:  # Tolerancia
                    print("DEBUG: Palmas tocándose... (tolerancia al flickering)")
                else:
                    print("DEBUG: Palmas tocándose interrumpidas, reseteando...")
                    self.menu_hold_start = None

        return None
