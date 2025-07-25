import cv2
import time
from mediapipe.python.solutions.hands import HandLandmark

class GestureDetector:
    def __init__(self):
        # Cooldowns separados por tipo de gesto
        # Estos cooldowns ayudan a evitar detecciones repetitivas
        self.pointing_cooldown = 0
        self.fist_cooldown = 0
        self.open_hand_cooldown = 0  
        self.cooldown_frames = 10  # Reducido aún más para mejor responsividad
        
        # Para gestos con tiempo sostenido
        self.rock_gesture_start_time = None
        self.peace_gesture_start_time = None
        self.rock_hold_duration = 2.0  # 2 segundos para rock
        self.peace_hold_duration = 1.2  # 1.2 segundos para peace
        
        # Tolerancia para flickering en gestos sostenidos
        # cuando se deja de detectar el gesto sostenido se espera un tiempo antes de resetear
        self.gesture_tolerance_time = 0.2  # 200ms de tolerancia
        
        # Estado actual del gesto detectado
        self.current_gesture = "ninguno"
        self.current_context_action = "nada"
        
        # Contador para estabilizar detección
        # wait 5 frames before resetting the gesture state
        self.no_gesture_frames = 0
        self.no_gesture_threshold = 5  # Frames sin gesto antes de resetear
        
    def update_cooldown(self):
        if self.pointing_cooldown > 0:
            self.pointing_cooldown -= 1
        if self.fist_cooldown > 0:
            self.fist_cooldown -= 1
        if self.open_hand_cooldown > 0:
            self.open_hand_cooldown -= 1
    
    def get_current_gesture_info(self):
        """Retorna el gesto actual y su acción en el contexto"""
        return self.current_gesture, self.current_context_action
    
    def update_gesture_state(self, gesture_name, context_action):
        """Actualiza el estado del gesto actual"""
        self.current_gesture = gesture_name
        self.current_context_action = context_action
        self.no_gesture_frames = 0  # Reset contador cuando se detecta gesto
    
    def reset_to_no_gesture(self):
        """Resetea el estado a ningún gesto"""
        self.current_gesture = "ninguno"
        self.current_context_action = "nada"
        print("DEBUG: Estado reseteado a 'ninguno'")
    
    def handle_no_gesture_detected(self):
        """Maneja el caso cuando no se detecta ningún gesto"""
        self.no_gesture_frames += 1
        if self.no_gesture_frames >= self.no_gesture_threshold:
            self.reset_to_no_gesture()
    
    def is_rock_sign(self, hand_landmarks):
        """Detecta el signo rock 🤟 (índice y menique extendidos, medio y anular doblados)"""
        index_tip = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_TIP]
        index_pip = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_PIP]
        
        middle_tip = hand_landmarks.landmark[HandLandmark.MIDDLE_FINGER_TIP]
        middle_pip = hand_landmarks.landmark[HandLandmark.MIDDLE_FINGER_PIP]
        
        ring_tip = hand_landmarks.landmark[HandLandmark.RING_FINGER_TIP]
        ring_pip = hand_landmarks.landmark[HandLandmark.RING_FINGER_PIP]
        
        pinky_tip = hand_landmarks.landmark[HandLandmark.PINKY_TIP]
        pinky_pip = hand_landmarks.landmark[HandLandmark.PINKY_PIP]
        
        # Threshold menos estricto
        threshold = 0.02  # Reducido de 0.03 a 0.02
        
        # Índice y menique extendidos (menos estricto)
        index_extended = index_tip.y < index_pip.y - threshold
        pinky_extended = pinky_tip.y < pinky_pip.y - threshold
        
        # Medio y anular doblados (menos estricto)
        middle_folded = middle_tip.y > middle_pip.y + threshold
        ring_folded = ring_tip.y > ring_pip.y + threshold
        
        # No importa el pulgar - solo verificar índice, medio, anular y menique
        return (index_extended and pinky_extended and middle_folded and ring_folded)
    
    def detect_timed_gestures(self, hand_landmarks, current_state):
        """Detecta gestos que requieren tiempo sostenido - versión robusta contra flickering"""
        current_time = time.time()
        
        # Verificar signo rock para cerrar programa
        if self.is_rock_sign(hand_landmarks):
            if self.rock_gesture_start_time is None:
                self.rock_gesture_start_time = current_time
                print("DEBUG: Iniciando contador rock...")
                self.update_gesture_state("signo rock", "manteniendo...")
            else:
                # Calcular tiempo transcurrido
                elapsed_time = current_time - self.rock_gesture_start_time
                if elapsed_time >= self.rock_hold_duration:
                    self.rock_gesture_start_time = None  # Reset
                    self.update_gesture_state("signo rock", "cerrar programa")
                    return "rock_hold"
                else:
                    # Mantener el estado durante la espera
                    remaining = self.rock_hold_duration - elapsed_time
                    self.update_gesture_state("signo rock", f"manteniendo... {remaining:.1f}s")
        else:
            # Solo resetear si han pasado algunos frames sin el gesto (tolerancia al flickering)
            if self.rock_gesture_start_time is not None:
                # Dar una pequena tolerancia de tiempo para el flickering
                time_since_start = current_time - self.rock_gesture_start_time
                if time_since_start < self.gesture_tolerance_time:  # Tolerancia
                    self.update_gesture_state("signo rock", "manteniendo... (tolerancia)")
                else:
                    print("DEBUG: Rock gesture interrumpido, reseteando...")
                    self.rock_gesture_start_time = None
        
        # Verificar signo de paz para toggle menú
        if self.is_peace_sign(hand_landmarks):
            if self.peace_gesture_start_time is None:
                self.peace_gesture_start_time = current_time
                print("DEBUG: Iniciando contador peace...")
                action = "ir al juego" if current_state == "MAIN_MENU" else "volver al menú"
                self.update_gesture_state("signo de paz", f"manteniendo... ({action})")
            else:
                # Calcular tiempo transcurrido
                elapsed_time = current_time - self.peace_gesture_start_time
                if elapsed_time >= self.peace_hold_duration:
                    self.peace_gesture_start_time = None  # Reset
                    action = "ir al juego" if current_state == "MAIN_MENU" else "volver al menú"
                    self.update_gesture_state("signo de paz", action)
                    return "peace_hold"
                else:
                    # Mantener el estado durante la espera
                    remaining = self.peace_hold_duration - elapsed_time
                    action = "ir al juego" if current_state == "MAIN_MENU" else "volver al menú"
                    self.update_gesture_state("signo de paz", f"manteniendo... {remaining:.1f}s ({action})")
        else:
            # Solo resetear si han pasado algunos frames sin el gesto (tolerancia al flickering)
            if self.peace_gesture_start_time is not None:
                # Dar una pequena tolerancia de tiempo para el flickering
                time_since_start = current_time - self.peace_gesture_start_time
                if time_since_start < self.gesture_tolerance_time:  # Tolerancia
                    action = "ir al juego" if current_state == "MAIN_MENU" else "volver al menú"
                    self.update_gesture_state("signo de paz", f"manteniendo... (tolerancia) ({action})")
                else:
                    print("DEBUG: Peace gesture interrumpido, reseteando...")
                    self.peace_gesture_start_time = None
        
        return None
    
    def is_peace_sign(self, hand_landmarks):
        """Detecta el signo de la paz (SOLO índice y medio arriba, anular y menique abajo)"""
        # Usar PIP joints para mayor precisión
        index_tip = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_TIP]
        index_pip = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_PIP]
        
        middle_tip = hand_landmarks.landmark[HandLandmark.MIDDLE_FINGER_TIP]
        middle_pip = hand_landmarks.landmark[HandLandmark.MIDDLE_FINGER_PIP]
        
        ring_tip = hand_landmarks.landmark[HandLandmark.RING_FINGER_TIP]
        ring_pip = hand_landmarks.landmark[HandLandmark.RING_FINGER_PIP]
        
        pinky_tip = hand_landmarks.landmark[HandLandmark.PINKY_TIP]
        pinky_pip = hand_landmarks.landmark[HandLandmark.PINKY_PIP]
        
        # Threshold menos estricto
        threshold = 0.02  # Reducido de 0.03 a 0.02
        
        # SOLO índice y medio extendidos (menos estricto)
        index_extended = index_tip.y < index_pip.y - threshold
        middle_extended = middle_tip.y < middle_pip.y - threshold
        
        # Anular y menique doblados (menos estricto)
        ring_folded = ring_tip.y > ring_pip.y + threshold
        pinky_folded = pinky_tip.y > pinky_pip.y + threshold
        
        # No importa el pulgar - solo verificar índice, medio, anular y menique
        return (index_extended and middle_extended and ring_folded and pinky_folded)
    
    def is_fist(self, hand_landmarks):
        """Detecta un puno - método mejorado con menos falsos positivos"""
        if self.fist_cooldown > 0:
            return False
            
        # Obtener landmarks relevantes
        index_tip = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_TIP]
        index_pip = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_PIP]
        index_mcp = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_MCP]
        
        middle_tip = hand_landmarks.landmark[HandLandmark.MIDDLE_FINGER_TIP]
        middle_pip = hand_landmarks.landmark[HandLandmark.MIDDLE_FINGER_PIP]
        middle_mcp = hand_landmarks.landmark[HandLandmark.MIDDLE_FINGER_MCP]
        
        ring_tip = hand_landmarks.landmark[HandLandmark.RING_FINGER_TIP]
        ring_pip = hand_landmarks.landmark[HandLandmark.RING_FINGER_PIP]
        ring_mcp = hand_landmarks.landmark[HandLandmark.RING_FINGER_MCP]
        
        pinky_tip = hand_landmarks.landmark[HandLandmark.PINKY_TIP]
        pinky_pip = hand_landmarks.landmark[HandLandmark.PINKY_PIP]
        pinky_mcp = hand_landmarks.landmark[HandLandmark.PINKY_MCP]
        
        # Verificar que TODOS los dedos estén claramente doblados
        # Los tips deben estar cerca o por debajo de los MCPs
        threshold = 0.02  # Más estricto
        
        # Calcular distancias verticales - todos deben estar doblados
        index_folded = index_tip.y >= index_mcp.y + threshold
        middle_folded = middle_tip.y >= middle_mcp.y + threshold  
        ring_folded = ring_tip.y >= ring_mcp.y + threshold
        pinky_folded = pinky_tip.y >= pinky_mcp.y + threshold
        
        # TODOS los dedos deben estar doblados para ser puno
        all_folded = index_folded and middle_folded and ring_folded and pinky_folded
        
        # Verificar que NO hay dedos claramente extendidos (anti-falso positivo más estricto)
        index_extended = index_tip.y < index_pip.y - 0.03
        middle_extended = middle_tip.y < middle_pip.y - 0.03
        ring_extended = ring_tip.y < ring_pip.y - 0.03
        pinky_extended = pinky_tip.y < pinky_pip.y - 0.03
        
        any_extended = index_extended or middle_extended or ring_extended or pinky_extended
        
        # Es puno solo si TODOS están doblados Y NINGUNO está extendido
        is_fist_gesture = all_folded and not any_extended
        
        if is_fist_gesture:
            self.fist_cooldown = self.cooldown_frames
            self.update_gesture_state("puno", "detectado")
            print(f"DEBUG: Puno detectado! Todos doblados: {all_folded}, Alguno extendido: {any_extended}")
            
        return is_fist_gesture
    
    def is_hand_open(self, hand_landmarks, current_state):
        """Detecta mano abierta - método mejorado y más confiable"""
        if self.open_hand_cooldown > 0:
            return False
            
        # Comparar tips con PIPs y MCPs para detectar extensión
        index_tip = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_TIP]
        index_pip = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_PIP]
        index_mcp = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_MCP]
        
        middle_tip = hand_landmarks.landmark[HandLandmark.MIDDLE_FINGER_TIP]
        middle_pip = hand_landmarks.landmark[HandLandmark.MIDDLE_FINGER_PIP]
        middle_mcp = hand_landmarks.landmark[HandLandmark.MIDDLE_FINGER_MCP]
        
        ring_tip = hand_landmarks.landmark[HandLandmark.RING_FINGER_TIP]
        ring_pip = hand_landmarks.landmark[HandLandmark.RING_FINGER_PIP]
        ring_mcp = hand_landmarks.landmark[HandLandmark.RING_FINGER_MCP]
        
        pinky_tip = hand_landmarks.landmark[HandLandmark.PINKY_TIP]
        pinky_pip = hand_landmarks.landmark[HandLandmark.PINKY_PIP]
        pinky_mcp = hand_landmarks.landmark[HandLandmark.PINKY_MCP]
        
        # Threshold más generoso para extensión
        pip_threshold = 0.02  # Para comparar con PIP
        mcp_threshold = 0.04  # Para comparar con MCP
        
        # Verificar extensión usando tanto PIP como MCP
        fingers_extended = []
        
        # Índice extendido si tip está claramente por encima de PIP y MCP
        if (index_tip.y < index_pip.y - pip_threshold and 
            index_tip.y < index_mcp.y - mcp_threshold):
            fingers_extended.append("index")
            
        # Medio extendido
        if (middle_tip.y < middle_pip.y - pip_threshold and 
            middle_tip.y < middle_mcp.y - mcp_threshold):
            fingers_extended.append("middle")
            
        # Anular extendido
        if (ring_tip.y < ring_pip.y - pip_threshold and 
            ring_tip.y < ring_mcp.y - mcp_threshold):
            fingers_extended.append("ring")
            
        # Menique extendido
        if (pinky_tip.y < pinky_pip.y - pip_threshold and 
            pinky_tip.y < pinky_mcp.y - mcp_threshold):
            fingers_extended.append("pinky")
        
        # Verificar que no hay dedos claramente doblados (anti-falso positivo)
        fingers_clearly_folded = []
        
        if index_tip.y > index_mcp.y + 0.01:
            fingers_clearly_folded.append("index")
        if middle_tip.y > middle_mcp.y + 0.01:
            fingers_clearly_folded.append("middle")
        if ring_tip.y > ring_mcp.y + 0.01:
            fingers_clearly_folded.append("ring")
        if pinky_tip.y > pinky_mcp.y + 0.01:
            fingers_clearly_folded.append("pinky")
        
        # Mano abierta si:
        # 1. Al menos 3 dedos están extendidos Y
        # 2. Máximo 1 dedo está claramente doblado
        is_open = len(fingers_extended) >= 3 and len(fingers_clearly_folded) <= 1
        
        if is_open:
            self.open_hand_cooldown = self.cooldown_frames
            action = "saltar" if current_state == "DINO_GAME" else "seleccionar"
            self.update_gesture_state("mano abierta", action)
            print(f"DEBUG: Mano abierta! Extendidos: {fingers_extended}, Doblados: {fingers_clearly_folded}")
        
        return is_open
    def is_pointing_up(self, hand_landmarks):
        """Detecta dedo índice apuntando hacia arriba"""
        if self.pointing_cooldown > 0:
            return False
            
        index_tip = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_TIP]
        index_pip = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_PIP]
        
        middle_tip = hand_landmarks.landmark[HandLandmark.MIDDLE_FINGER_TIP]
        middle_pip = hand_landmarks.landmark[HandLandmark.MIDDLE_FINGER_PIP]
        
        ring_tip = hand_landmarks.landmark[HandLandmark.RING_FINGER_TIP]
        ring_pip = hand_landmarks.landmark[HandLandmark.RING_FINGER_PIP]
        
        pinky_tip = hand_landmarks.landmark[HandLandmark.PINKY_TIP]
        pinky_pip = hand_landmarks.landmark[HandLandmark.PINKY_PIP]
        
        threshold = 0.025  # Menos estricto
        
        # Índice extendido hacia arriba
        index_extended = index_tip.y < index_pip.y - threshold
        
        # Otros dedos no tan extendidos
        middle_not_extended = middle_tip.y > middle_pip.y - threshold/2
        ring_not_extended = ring_tip.y > ring_pip.y - threshold/2
        pinky_not_extended = pinky_tip.y > pinky_pip.y - threshold/2
        
        is_pointing = (index_extended and middle_not_extended and 
                      ring_not_extended and pinky_not_extended)
        
        if is_pointing:
            self.pointing_cooldown = self.cooldown_frames
            self.update_gesture_state("apuntar arriba", "opción anterior")
            print("DEBUG: Apuntar arriba detectado!")  # Debug
            
        return is_pointing
    
    def is_pointing_down(self, hand_landmarks):
        """Detecta dedo índice apuntando hacia abajo"""
        if self.pointing_cooldown > 0:
            return False
            
        # Obtener la muneca como referencia
        wrist = hand_landmarks.landmark[HandLandmark.WRIST]
        index_tip = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_TIP]
        index_pip = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_PIP]
        
        middle_tip = hand_landmarks.landmark[HandLandmark.MIDDLE_FINGER_TIP]
        middle_pip = hand_landmarks.landmark[HandLandmark.MIDDLE_FINGER_PIP]
        
        ring_tip = hand_landmarks.landmark[HandLandmark.RING_FINGER_TIP]
        ring_pip = hand_landmarks.landmark[HandLandmark.RING_FINGER_PIP]
        
        pinky_tip = hand_landmarks.landmark[HandLandmark.PINKY_TIP]
        pinky_pip = hand_landmarks.landmark[HandLandmark.PINKY_PIP]
        
        threshold = 0.025
        
        # Índice apuntando hacia abajo
        index_pointing_down = (index_tip.y > wrist.y + threshold and 
                              index_tip.y > index_pip.y + threshold)
        
        # Otros dedos no tan extendidos
        middle_not_extended = middle_tip.y > middle_pip.y - threshold/2
        ring_not_extended = ring_tip.y > ring_pip.y - threshold/2
        pinky_not_extended = pinky_tip.y > pinky_pip.y - threshold/2
        
        is_pointing = (index_pointing_down and middle_not_extended and 
                      ring_not_extended and pinky_not_extended)
        
        if is_pointing:
            self.pointing_cooldown = self.cooldown_frames
            self.update_gesture_state("apuntar abajo", "siguiente opción")
            print("DEBUG: Apuntar abajo detectado!")  # Debug
            
        return is_pointing
    
    def is_pinky_up(self, hand_landmarks):
        """Detecta meñique levantado (los otros 3 dedos abajo)"""
        if self.pointing_cooldown > 0:
            return False
            
        # Obtener landmarks relevantes
        index_tip = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_TIP]
        index_pip = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_PIP]
        
        middle_tip = hand_landmarks.landmark[HandLandmark.MIDDLE_FINGER_TIP]
        middle_pip = hand_landmarks.landmark[HandLandmark.MIDDLE_FINGER_PIP]
        
        ring_tip = hand_landmarks.landmark[HandLandmark.RING_FINGER_TIP]
        ring_pip = hand_landmarks.landmark[HandLandmark.RING_FINGER_PIP]
        
        pinky_tip = hand_landmarks.landmark[HandLandmark.PINKY_TIP]
        pinky_pip = hand_landmarks.landmark[HandLandmark.PINKY_PIP]
        
        threshold = 0.025
        
        # Meñique extendido hacia arriba
        pinky_extended = pinky_tip.y < pinky_pip.y - threshold
        
        # Otros dedos no tan extendidos (doblados)
        index_not_extended = index_tip.y > index_pip.y - threshold/2
        middle_not_extended = middle_tip.y > middle_pip.y - threshold/2
        ring_not_extended = ring_tip.y > ring_pip.y - threshold/2
        
        is_pinky_gesture = (pinky_extended and index_not_extended and 
                           middle_not_extended and ring_not_extended)
        
        if is_pinky_gesture:
            self.pointing_cooldown = self.cooldown_frames
            self.update_gesture_state("meñique arriba", "izquierda")
            print("DEBUG: Meñique arriba detectado!")
            
        return is_pinky_gesture

    def is_thumb_left(self, hand_landmarks):
        # Esta función ya no se usa para el laberinto
        # Se mantiene por compatibilidad con otros juegos si es necesario
        thumb_tip = hand_landmarks.landmark[4]
        thumb_ip = hand_landmarks.landmark[3]
        thumb_mcp = hand_landmarks.landmark[2]
        
        other_tips = [hand_landmarks.landmark[i] for i in [8, 12, 16, 20]]
        other_mcps = [hand_landmarks.landmark[i-2] for i in [8, 12, 16, 20]]

        threshold = 0.025
        
        thumb_extended_left = (thumb_tip.x < thumb_ip.x - threshold and
                                thumb_tip.x < thumb_mcp.x - threshold)
        
        others_folded = all(t.y > m.y for t, m in zip(other_tips, other_mcps))

        if thumb_extended_left and others_folded:
            self.update_gesture_state("pulgar izquierda", "izquierda")
            self.pointing_cooldown = self.cooldown_frames
            return True
        return False

    def is_thumb_right(self, hand_landmarks):
        thumb_tip = hand_landmarks.landmark[4]
        thumb_ip = hand_landmarks.landmark[3]
        thumb_mcp = hand_landmarks.landmark[2]

        other_tips = [hand_landmarks.landmark[i] for i in [8, 12, 16, 20]]
        other_mcps = [hand_landmarks.landmark[i-2] for i in [8, 12, 16, 20]]

        threshold = 0.025

        thumb_extended_right = (thumb_tip.x > thumb_ip.x + threshold and
                                thumb_tip.x > thumb_mcp.x + threshold)

        others_folded = all(t.y > m.y for t, m in zip(other_tips, other_mcps))

        if thumb_extended_right and others_folded:
            self.update_gesture_state("pulgar derecha", "derecha")
            self.pointing_cooldown = self.cooldown_frames
            return True
        return False
