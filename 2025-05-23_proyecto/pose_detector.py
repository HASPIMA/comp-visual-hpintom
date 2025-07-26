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
        
        # Estado actual del gesto detectado (para debugging y UI)
        self.current_pose_action = "ninguna"
        self.current_pose_description = "esperando..."
        
        # Tracking de estado para transiciones (evitar spam y manejar press/release)
        self.last_movement_action = None  # Última acción de movimiento detectada
        self.last_jump_action = None
        self.last_attack_action = None

    def get_current_pose_info(self):
        """Retorna el gesto actual y su descripción para mostrar en UI"""
        return self.current_pose_action, self.current_pose_description
    
    def update_pose_state(self, action, description):
        """Actualiza el estado del gesto actual"""
        self.current_pose_action = action
        self.current_pose_description = description

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

        # LEFT/RIGHT tilt - parámetros menos estrictos con manejo de transiciones
        shoulder_diff_left = right_shoulder.y - left_shoulder.y
        shoulder_diff_right = left_shoulder.y - right_shoulder.y
        tilt_threshold = 0.08  # Reducido de 0.2 a 0.08 (más sensible)
        
        current_movement = None
        
        if shoulder_diff_left > tilt_threshold:
            current_movement = "left"
            self.update_pose_state("inclinacion_izquierda", f"Moviendo LEFT (diff: {shoulder_diff_left:.3f})")
            print(f"DEBUG POSE: Inclinación izquierda detectada (diff: {shoulder_diff_left:.3f})")
        elif shoulder_diff_right > tilt_threshold:
            current_movement = "right"
            self.update_pose_state("inclinacion_derecha", f"Moviendo RIGHT (diff: {shoulder_diff_right:.3f})")
            print(f"DEBUG POSE: Inclinación derecha detectada (diff: {shoulder_diff_right:.3f})")
        
        # Manejar transiciones de movimiento
        if current_movement != self.last_movement_action:
            # Cambio de estado detectado
            if self.last_movement_action is not None:
                # Soltar la tecla anterior si había una presionada
                print(f"DEBUG POSE: Soltando tecla: {self.last_movement_action}")
                result = f"release_{self.last_movement_action}"
                self.last_movement_action = current_movement
                return result
            
            if current_movement is not None:
                # Presionar nueva tecla
                print(f"DEBUG POSE: Presionando tecla: {current_movement}")
                self.last_movement_action = current_movement
                return f"press_{current_movement}"
        
        # Si no hay cambio de movimiento, continuar con otros gestos

        # JUMP (both hands near knees) - con cooldown para evitar spam
        left_knee_dist = abs(left_wrist.y - left_knee.y)
        right_knee_dist = abs(right_wrist.y - right_knee.y)
        knee_threshold = 0.18  # Incrementado de 0.1 a 0.18 (más fácil)
        
        hands_near_knees = (left_knee_dist < knee_threshold and right_knee_dist < knee_threshold)
        if hands_near_knees and self.last_jump_action != "x":
            # Solo activar si no estaba activado antes (evitar spam)
            self.last_jump_action = "x"
            self.update_pose_state("salto", f"SALTO detectado (dist_izq: {left_knee_dist:.3f}, dist_der: {right_knee_dist:.3f})")
            print(f"DEBUG POSE: Manos cerca rodillas (dist_izq: {left_knee_dist:.3f}, dist_der: {right_knee_dist:.3f})")
            return "x"
        elif not hands_near_knees:
            # Reset del estado de salto cuando no se detecta
            self.last_jump_action = None

        # Z: arm lifted above clavicle/neck area - con cooldown para evitar spam
        clavicle_y = (left_shoulder.y + right_shoulder.y) / 2
        arm_threshold = 0.05  # Un poco arriba de la clavícula
        
        left_wrist_above_clavicle = left_wrist.y < (clavicle_y - arm_threshold)
        right_wrist_above_clavicle = right_wrist.y < (clavicle_y - arm_threshold)
        
        arm_raised = left_wrist_above_clavicle or right_wrist_above_clavicle
        if arm_raised and self.last_attack_action != "z":
            # Solo activar si no estaba activado antes (evitar spam)
            self.last_attack_action = "z"
            arm_side = "izquierda" if left_wrist_above_clavicle else "derecha"
            wrist_y = left_wrist.y if left_wrist_above_clavicle else right_wrist.y
            self.update_pose_state("brazo_arriba", f"ATAQUE - brazo {arm_side} arriba (muñeca: {wrist_y:.3f}, clavícula: {clavicle_y:.3f})")
            print(f"DEBUG POSE: Brazo {arm_side} arriba detectado (muñeca: {wrist_y:.3f}, clavícula: {clavicle_y:.3f})")
            return "z"
        elif not arm_raised:
            # Reset del estado de ataque cuando no se detecta
            self.last_attack_action = None

        # MENU: palmas tocándose por 3 segundos (con tolerancia al flickering)
        if self.are_palms_touching(left_wrist, right_wrist):
            if self.menu_hold_start is None:
                self.menu_hold_start = current_time
                self.update_pose_state("palmas_tocandose", "Iniciando contador palmas...")
                print("DEBUG POSE: Iniciando contador palmas tocándose...")
            elif current_time - self.menu_hold_start > self.menu_hold_duration:
                self.update_pose_state("palmas_tocandose", "IR AL MENÚ - palmas mantenidas")
                print("DEBUG POSE: Palmas tocándose mantenidas por 3 segundos - ir al menú")
                self.menu_hold_start = None  # Reset para evitar repetición
                return "menu"
            else:
                remaining = self.menu_hold_duration - (current_time - self.menu_hold_start)
                self.update_pose_state("palmas_tocandose", f"Palmas tocándose... {remaining:.1f}s restantes")
                print(f"DEBUG POSE: Palmas tocándose... {remaining:.1f}s restantes")
        else:
            # Solo resetear si han pasado algunos frames sin el gesto (tolerancia al flickering)
            if self.menu_hold_start is not None:
                # Dar una pequeña tolerancia de tiempo para el flickering
                time_since_start = current_time - self.menu_hold_start
                if time_since_start < self.gesture_tolerance_time:  # Tolerancia
                    self.update_pose_state("palmas_tocandose", "Tolerancia al flickering...")
                    print("DEBUG POSE: Palmas tocándose... (tolerancia al flickering)")
                else:
                    self.update_pose_state("ninguna", "Palmas interrumpidas, reseteando...")
                    print("DEBUG POSE: Palmas tocándose interrumpidas, reseteando...")
                    self.menu_hold_start = None

        # Si no se detectó ningún gesto, actualizar estado
        self.update_pose_state("ninguna", "Esperando gesto...")
        return None
