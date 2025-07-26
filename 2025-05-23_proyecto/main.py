import cv2
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions.hands import HAND_CONNECTIONS, Hands
from mediapipe.python.solutions.pose import Pose, POSE_CONNECTIONS


from game_states import GameState
from gesture_detector import GestureDetector
from pose_detector import PoseDetector
from menu_renderer import MenuRenderer
from dino_game import DinoGame
from laberinto_game import LaberintoGame
from hollow_knight import HollowKnightGame

class GestureGameApp:
    def __init__(self):
        #use 0 for the default camera
        #use 1 for the external camera
        self.camera_index = 1
        self.cap = cv2.VideoCapture(self.camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.hands = Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.pose = Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False)

        self.current_state = GameState.MAIN_MENU
        self.gesture_detector = GestureDetector()
        self.pose_detector = PoseDetector()
        self.menu_renderer = MenuRenderer()
        self.dino_game = DinoGame()
        self.laberinto_game = LaberintoGame()
        self.hollow_knight_game = HollowKnightGame()

        self.state_change_cooldown = 0

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        frame = cv2.flip(frame, 1)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hand_results = self.hands.process(image_rgb)
        pose_results = self.pose.process(image_rgb)
        # print(GameState.__members__)  # imprime todos los miembros del Enum

        if self.current_state == GameState.HOLLOW_KNIGHT:
            if pose_results.pose_landmarks:
                # 🔽 Dibuja los landmarks sobre el frame
                mp_drawing.draw_landmarks(
                    frame,
                    pose_results.pose_landmarks,
                    POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 100, 255), thickness=2),
                )

                # 🔽 Procesa la acción
                action = self.pose_detector.detect_action(pose_results.pose_landmarks.landmark)
                if action:
                    result = self.hollow_knight_game.handle_pose_output(action)
                    if result == "menu":
                        self.current_state = GameState.MAIN_MENU

        else:
            self.gesture_detector.update_cooldown()
            if self.state_change_cooldown > 0:
                self.state_change_cooldown -= 1
            if hand_results.multi_hand_landmarks:
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, list(HAND_CONNECTIONS)
                    )
                    self.handle_gestures(hand_landmarks, frame)
            else:
                self.gesture_detector.handle_no_gesture_detected()

        frame = self.render_ui(frame)
        return frame

    def handle_gestures(self, hand_landmarks, frame):
        current_state_str = self.current_state.value.upper()
        gesture_detected = False

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
                    if selected_game == 0:
                        self.current_state = GameState.DINO_GAME
                    elif selected_game == 1:
                        self.current_state = GameState.LABERINTO_GAME
                    elif selected_game == 2:
                        self.current_state = GameState.HOLLOW_KNIGHT
                else:
                    self.current_state = GameState.MAIN_MENU
                return

        if self.current_state == GameState.MAIN_MENU:
            if self.handle_menu_gestures(hand_landmarks):
                gesture_detected = True
        elif self.current_state == GameState.DINO_GAME:
            if self.handle_dino_gestures(hand_landmarks):
                gesture_detected = True
        elif self.current_state == GameState.LABERINTO_GAME:
            if self.handle_laberinto_gestures(hand_landmarks):
                gesture_detected = True

        if not gesture_detected:
            self.gesture_detector.handle_no_gesture_detected()

    def handle_menu_gestures(self, hand_landmarks):
        if self.gesture_detector.is_pointing_up(hand_landmarks):
            self.menu_renderer.navigate_up()
            return True
        elif self.gesture_detector.is_pointing_down(hand_landmarks):
            self.menu_renderer.navigate_down()
            return True
        elif self.gesture_detector.is_hand_open(hand_landmarks, "MAIN_MENU"):
            selected_game = self.menu_renderer.get_selected_game()
            if selected_game == 0:
                print("Selected Dinosaur Game")
                self.current_state = GameState.DINO_GAME
            elif selected_game == 1:
                print("Selected Laberinto Game")
                self.current_state = GameState.LABERINTO_GAME
            elif selected_game == 2:
                print("Selected Hollow Knight Game")
                self.current_state = GameState.HOLLOW_KNIGHT
            return True
        elif self.gesture_detector.is_fist(hand_landmarks):
            return True
        return False

    def handle_dino_gestures(self, hand_landmarks):
        if self.gesture_detector.is_hand_open(hand_landmarks, "DINO_GAME"):
            jumped = self.dino_game.handle_gesture(True)
            if jumped:
                print("Jump!")
            return True
        elif self.gesture_detector.is_fist(hand_landmarks):
            return True
        return False

    def handle_laberinto_gestures(self, hand_landmarks):
        if self.gesture_detector.is_pointing_up(hand_landmarks):
            return self.laberinto_game.handle_gesture("up")
        elif self.gesture_detector.is_hand_open(hand_landmarks, "LABERINTO_GAME"):
            return self.laberinto_game.handle_gesture("down")
        elif self.gesture_detector.is_pinky_up(hand_landmarks):
            return self.laberinto_game.handle_gesture("left")
        elif self.gesture_detector.is_thumb_right(hand_landmarks):
            return self.laberinto_game.handle_gesture("right")
        return False

    def render_ui(self, frame):
        if self.current_state == GameState.MAIN_MENU:
            frame = self.menu_renderer.draw_menu(frame)
        elif self.current_state == GameState.DINO_GAME:
            frame = self.dino_game.draw_info(frame)
        elif self.current_state == GameState.LABERINTO_GAME:
            frame = self.laberinto_game.draw_info(frame)
        elif self.current_state == GameState.HOLLOW_KNIGHT:
            frame = self.hollow_knight_game.draw_info(frame, self.pose_detector)

        cv2.putText(frame, f"Estado: {self.current_state.value}",
                   (frame.shape[1] - 200, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)

        gesture, action = self.gesture_detector.get_current_gesture_info()
        gesture_text = f"{gesture} ({action})"
        text_x = frame.shape[1] - 350
        text_y = frame.shape[0] - 30

        text_size = cv2.getTextSize(gesture_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
        cv2.rectangle(frame, (text_x - 5, text_y - text_size[1] - 5),
                     (text_x + text_size[0] + 5, text_y + 5), (0, 0, 0), -1)

        color = (0, 255, 0) if gesture != "ninguno" else (100, 100, 100)
        cv2.putText(frame, gesture_text, (text_x, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)

        return frame

    def run(self):
        print("¡Aplicación de Juegos por Gestos Iniciada!")
        print("Controles:")
        print("- Signo rock 🤟 (2s): Cerrar programa")
        print("- Signo de paz ✌️ (1.2s): Cambiar entre menú y juego")
        print("- Apuntar arriba ☝️: Opción anterior")
        print("- Apuntar abajo 👇: Siguiente opción")
        print("- Mano abierta 🖐️: Seleccionar / Mover abajo")
        print("- Pulgar izquierdo 👈: Mover izquierda")
        print("- Pulgar derecho 👉: Mover derecha")
        print("- Presiona 'q' para salir")

        while self.current_state != GameState.CLOSED:
            frame = self.process_frame()
            if frame is None:
                break
            cv2.imshow('Gesture Game Hub', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        print("Application closed.")

if __name__ == "__main__":
    app = GestureGameApp()
    app.run()
