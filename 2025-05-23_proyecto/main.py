import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
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
# from metrics_collector import MetricsCollector  # DESHABILITADO

class GestureGameApp:
    def __init__(self):
        # Configurar ventana de tkinter
        self.root = tk.Tk()
        self.root.title("🎮 GESTIK - Control por Gestos")
        self.root.geometry("1280x720")
        
        # Intentar cargar icono (si existe)
        try:
            # Cargar icono PNG y convertir para tkinter
            icon_image = Image.open("icon.png")
            # Redimensionar si es muy grande (máximo 64x64 para el icono)
            icon_image = icon_image.resize((64, 64), Image.Resampling.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.root.iconphoto(True, icon_photo)
        except Exception as e:
            print(f"Icono no encontrado: {e}, usando icono por defecto")
        
        # Configurar canvas para mostrar video
        self.canvas = tk.Canvas(self.root, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Variables de control
        self.running = True
        
        # Configurar cámara
        self.camera_index = 0  # Fijo en cámara 1 como solicitaste
        self.cap = cv2.VideoCapture(self.camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Configurar MediaPipe
        self.hands = Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.pose = Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False)

        # Configurar estados del juego
        self.current_state = GameState.MAIN_MENU
        self.gesture_detector = GestureDetector()
        self.pose_detector = PoseDetector()
        self.menu_renderer = MenuRenderer()
        self.dino_game = DinoGame()
        self.laberinto_game = LaberintoGame()
        self.hollow_knight_game = HollowKnightGame()

        # Inicializar sistema de métricas
        # self.metrics = MetricsCollector()  # DESHABILITADO
        
        self.state_change_cooldown = 0
        
        # Configurar eventos de cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        print("Cerrando aplicación...")
        self.running = False
        
        # Generar reporte de métricas antes de cerrar
        # if hasattr(self, 'metrics'):
        #     self.metrics.generate_report()  # DESHABILITADO
        
        if self.cap:
            self.cap.release()
        # Liberar recursos de MediaPipe
        if hasattr(self, 'hands'):
            self.hands.close()
        if hasattr(self, 'pose'):
            self.pose.close()
        # Cerrar ventana de tkinter
        try:
            self.root.quit()  # Salir del mainloop
            self.root.destroy()  # Destruir la ventana
        except:
            pass

    def convert_cv2_to_tkinter(self, cv2_image):
        """Convierte imagen de OpenCV a formato compatible con tkinter"""
        # Convertir de BGR a RGB
        rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        
        # Convertir a PIL Image
        pil_image = Image.fromarray(rgb_image)
        
        # Obtener tamaño del canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Si el canvas aún no tiene tamaño, usar tamaño por defecto
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width, canvas_height = 1280, 720
        
        # Redimensionar manteniendo aspect ratio
        img_width, img_height = pil_image.size
        aspect_ratio = img_width / img_height
        canvas_aspect_ratio = canvas_width / canvas_height
        
        if aspect_ratio > canvas_aspect_ratio:
            # La imagen es más ancha
            new_width = canvas_width
            new_height = int(canvas_width / aspect_ratio)
        else:
            # La imagen es más alta
            new_height = canvas_height
            new_width = int(canvas_height * aspect_ratio)
        
        # Redimensionar imagen
        pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convertir a ImageTk
        tk_image = ImageTk.PhotoImage(pil_image)
        
        return tk_image, new_width, new_height

    def update_frame(self):
        """Actualiza el frame de video en la ventana de tkinter"""
        if not self.running:
            return
            
        frame = self.process_frame()
        
        if frame is not None:
            try:
                # Convertir frame para tkinter
                tk_image, img_width, img_height = self.convert_cv2_to_tkinter(frame)
                
                # Limpiar canvas
                self.canvas.delete("all")
                
                # Centrar imagen en canvas
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                x = (canvas_width - img_width) // 2
                y = (canvas_height - img_height) // 2
                
                # Mostrar imagen
                self.canvas.create_image(x, y, anchor=tk.NW, image=tk_image)
                
                # Mantener referencia para evitar garbage collection
                self.canvas.image = tk_image
                
            except Exception as e:
                print(f"Error actualizando frame: {e}")
        
        # Programar siguiente actualización
        if self.running:
            self.root.after(30, self.update_frame)  # ~33 FPS

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        # Registrar métricas de frame
        # if hasattr(self, 'metrics'):
        #     self.metrics.record_frame()
        #     self.metrics.record_system_resources()  # DESHABILITADO

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
                self.on_closing()  # Cerrar realmente la aplicación
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
        """Inicia la aplicación con interfaz tkinter"""
        print("🎮 ¡GESTIK - Control por Gestos Iniciado!")
        print("Controles:")
        print("- Signo rock 🤟 (2s): Cerrar programa")
        print("- Signo de paz ✌️ (1.2s): Cambiar entre menú y juego")
        print("- Apuntar arriba ☝️: Opción anterior")
        print("- Apuntar abajo 👇: Siguiente opción")
        print("- Mano abierta 🖐️: Seleccionar / Saltar")
        print("- Meñique arriba 🤙: Mover izquierda")
        print("- Pulgar derecho 👉: Mover derecha")
        print("- Cierra la ventana con X para salir")
        print("- Ventana redimensionable: Puedes cambiar el tamaño!")
        
        # Iniciar actualización de frames
        self.update_frame()
        
        # Iniciar loop principal de tkinter
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Interrumpido por usuario")
        finally:
            self.cleanup()

    def cleanup(self):
        """Limpia recursos al cerrar la aplicación"""
        print("Cerrando aplicación...")
        self.running = False
        if hasattr(self, 'cap') and self.cap:
            self.cap.release()
        if hasattr(self, 'hands'):
            self.hands.close()
        if hasattr(self, 'pose'):
            self.pose.close()
        print("✅ GESTIK cerrado correctamente.")

if __name__ == "__main__":
    app = GestureGameApp()
    app.run()
