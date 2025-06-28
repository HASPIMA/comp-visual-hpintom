import cv2
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions.hands import HAND_CONNECTIONS, Hands

from game_states import GameState
from gesture_detector import GestureDetector
from menu_renderer import MenuRenderer
from dino_game import DinoGame

class GestureGameApp:
    def __init__(self):
        self.camera_index = 0
        self.cap = cv2.VideoCapture(self.camera_index)
        
        # Configurar tamaño de la ventana más grande
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        self.hands = Hands(
            static_image_mode=False,
            max_num_hands=1,  # Volvemos a una sola mano
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        
        # Estados y componentes
        self.current_state = GameState.MAIN_MENU
        self.gesture_detector = GestureDetector()
        self.menu_renderer = MenuRenderer()
        self.dino_game = DinoGame()
        
        # Control de gestos para cambio de estado
        self.state_change_cooldown = 0
        
    def process_frame(self):
        """Procesa un frame de la cámara"""
        ret, frame = self.cap.read()
        if not ret:
            return None
            
        # Flip horizontal para efecto espejo
        frame = cv2.flip(frame, 1)
        
        # Convertir a RGB para MediaPipe
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        
        # Actualizar cooldowns
        self.gesture_detector.update_cooldown()
        if self.state_change_cooldown > 0:
            self.state_change_cooldown -= 1
        
        # Procesar detecciones de manos
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Dibujar landmarks
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, list(HAND_CONNECTIONS)
                )
                
                # Procesar gestos según el estado actual
                self.handle_gestures(hand_landmarks, frame)
        else:
            # Si no hay manos, manejar ausencia de gesto
            self.gesture_detector.handle_no_gesture_detected()
        
        # Renderizar UI según el estado
        frame = self.render_ui(frame)
        
        return frame
    
    def handle_gestures(self, hand_landmarks, frame):
        """Maneja los gestos según el estado actual"""
        current_state_str = self.current_state.value.upper()
        gesture_detected = False
        
        # Verificar gestos sostenidos (rock y peace)
        timed_gesture = self.gesture_detector.detect_timed_gestures(
            hand_landmarks, current_state_str
        )
        
        if timed_gesture:
            gesture_detected = True
            if timed_gesture == "rock_hold":
                print("Rock sign held for 2s - Closing program")
                self.current_state = GameState.CLOSED
                return
            elif timed_gesture == "peace_hold":
                print("Peace sign held for 1.2s - Toggling menu")
                if self.current_state == GameState.MAIN_MENU:
                    selected_game = self.menu_renderer.get_selected_game()
                    if selected_game == 0:  # Dinosaur Game
                        self.current_state = GameState.DINO_GAME
                else:
                    self.current_state = GameState.MAIN_MENU
                return
        
        # Gestos instantáneos específicos por estado
        if self.current_state == GameState.MAIN_MENU:
            if self.handle_menu_gestures(hand_landmarks):
                gesture_detected = True
        elif self.current_state == GameState.DINO_GAME:
            if self.handle_dino_gestures(hand_landmarks):
                gesture_detected = True
        
        # Si no se detectó ningún gesto específico
        if not gesture_detected:
            self.gesture_detector.handle_no_gesture_detected()
    
    def handle_menu_gestures(self, hand_landmarks):
        """Maneja gestos en el menú - retorna True si se detectó un gesto"""
        if self.gesture_detector.is_pointing_up(hand_landmarks):
            self.menu_renderer.navigate_up()
            return True
        elif self.gesture_detector.is_pointing_down(hand_landmarks):
            self.menu_renderer.navigate_down()
            return True
        elif self.gesture_detector.is_hand_open(hand_landmarks, "MAIN_MENU"):
            selected_game = self.menu_renderer.get_selected_game()
            if selected_game == 0:  # Dinosaur Game
                print("Selected Dinosaur Game")
                self.current_state = GameState.DINO_GAME
            return True
        elif self.gesture_detector.is_fist(hand_landmarks):
            # Puño detectado pero no hace nada (solo para logging)
            return True
        return False
    
    def handle_dino_gestures(self, hand_landmarks):
        """Maneja gestos en el juego del dinosaurio - retorna True si se detectó un gesto"""
        if self.gesture_detector.is_hand_open(hand_landmarks, "DINO_GAME"):
            jumped = self.dino_game.handle_gesture(True)
            if jumped:
                print("Jump!")
            return True
        elif self.gesture_detector.is_fist(hand_landmarks):
            # Puño detectado pero no hace nada (solo para logging)
            return True
        return False
    
    def render_ui(self, frame):
        """Renderiza la UI según el estado actual"""
        if self.current_state == GameState.MAIN_MENU:
            frame = self.menu_renderer.draw_menu(frame)
        elif self.current_state == GameState.DINO_GAME:
            frame = self.dino_game.draw_info(frame)
        
        # Mostrar estado actual en la esquina superior derecha
        cv2.putText(frame, f"Estado: {self.current_state.value}", 
                   (frame.shape[1] - 200, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
        
        # Mostrar información del gesto actual en la esquina inferior derecha
        gesture, action = self.gesture_detector.get_current_gesture_info()
        gesture_text = f"{gesture} ({action})"
        
        # Calcular posición del texto
        text_x = frame.shape[1] - 350
        text_y = frame.shape[0] - 30
        
        # Fondo semi-transparente para el texto del gesto
        text_size = cv2.getTextSize(gesture_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
        cv2.rectangle(frame, (text_x - 5, text_y - text_size[1] - 5), 
                     (text_x + text_size[0] + 5, text_y + 5), (0, 0, 0), -1)
        
        # Texto del gesto con colores según el tipo
        color = (0, 255, 0) if gesture != "ninguno" else (100, 100, 100)
        cv2.putText(frame, gesture_text, (text_x, text_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)
        
        return frame
    
    def run(self):
        """Loop principal de la aplicación"""
        print("¡Aplicación de Juegos por Gestos Iniciada!")
        print("Controles:")
        print("- Signo rock 🤟 (2s): Cerrar programa")
        print("- Signo de paz ✌️ (1.2s): Cambiar entre menú y juego")
        print("- Apuntar arriba ☝️: Opción anterior")
        print("- Apuntar abajo 👇: Siguiente opción")
        print("- Mano abierta 🖐️: Seleccionar/Saltar")
        print("- Presiona 'q' para salir")
        
        while self.current_state != GameState.CLOSED:
            frame = self.process_frame()
            if frame is None:
                break
                
            cv2.imshow('Gesture Game Hub', frame)
            
            # Permitir salir con 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cleanup()
    
    def cleanup(self):
        """Limpia recursos"""
        self.cap.release()
        cv2.destroyAllWindows()
        print("Application closed.")

if __name__ == "__main__":
    app = GestureGameApp()
    app.run()
