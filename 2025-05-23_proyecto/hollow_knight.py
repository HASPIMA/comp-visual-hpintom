# hollow_knight.py
import time
import cv2
import keyboard
import threading

class HollowKnightGame:
    def __init__(self):
        self.last_jump_time = 0
        self.jump_cooldown = 0.8  # Reducido para permitir saltos más frecuentes
        self.last_z_time = 0
        self.z_cooldown = 0.3  # Reducido para ataques más responsivos
        
        # Estado de teclas presionadas para evitar conflictos
        self.keys_pressed = {
            "left": False,
            "right": False
        }

    def handle_pose_output(self, action):
        """
        Ejecuta una acción basada en el gesto detectado por pose_detector
        Maneja los nuevos comandos press/release
        """
        current_time = time.time()
        
        # Manejar comandos de movimiento con press/release
        if action == "press_left":
            if not self.keys_pressed["left"]:
                keyboard.press("left")
                self.keys_pressed["left"] = True
                print("DEBUG HK: Presionando LEFT")
            return True
            
        elif action == "release_left":
            if self.keys_pressed["left"]:
                keyboard.release("left")
                self.keys_pressed["left"] = False
                print("DEBUG HK: Soltando LEFT")
            return True
            
        elif action == "press_right":
            if not self.keys_pressed["right"]:
                keyboard.press("right")
                self.keys_pressed["right"] = True
                print("DEBUG HK: Presionando RIGHT")
            return True
            
        elif action == "release_right":
            if self.keys_pressed["right"]:
                keyboard.release("right")
                self.keys_pressed["right"] = False
                print("DEBUG HK: Soltando RIGHT")
            return True
        
        # Compatibilidad con comandos antiguos (por si acaso)
        elif action == "left":
            return self.handle_pose_output("press_left")
        elif action == "right":
            return self.handle_pose_output("press_right")
        elif action == "release":
            # Soltar ambas teclas
            if self.keys_pressed["left"]:
                self.handle_pose_output("release_left")
            if self.keys_pressed["right"]:
                self.handle_pose_output("release_right")
            return True
            
        elif action == "z":
            if current_time - self.last_z_time > self.z_cooldown:
                keyboard.press_and_release("z")
                self.last_z_time = current_time
                print("DEBUG HK: Ataque Z")
                return True
                
        elif action == "x":
            if current_time - self.last_jump_time > self.jump_cooldown:
                # Salto con duración para alcanzar 60% de altura
                # Hold por ~0.25 segundos según documentación de Hollow Knight
                keyboard.press("x")
                print("DEBUG HK: Iniciando salto (hold 0.25s para 60% altura)")
                
                # Programar release después de 0.25s
                def release_jump():
                    keyboard.release("x")
                    print("DEBUG HK: Finalizando salto")
                
                threading.Timer(0.25, release_jump).start()
                self.last_jump_time = current_time
                return True
                
        elif action == "menu":
            # Asegurar que no hay teclas quedadas presionadas al salir
            self.release_all_keys()
            return "menu"
            
        return False
    
    def release_all_keys(self):
        """Suelta todas las teclas que podrían estar presionadas"""
        for key in ["left", "right", "x", "z"]:
            try:
                keyboard.release(key)
            except:
                pass  # Ignorar errores si la tecla no estaba presionada
        
        self.keys_pressed = {"left": False, "right": False}
        print("DEBUG HK: Todas las teclas liberadas")

    def draw_info(self, frame, pose_detector=None):
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

        put("HOLLOW KNIGHT (control corporal MEJORADO)", (0, 255, 255))
        put("Inclinar hombros izquierda:      LEFT (press/release)")
        put("Inclinar hombros derecha:        RIGHT (press/release)")
        put("Levantar brazo arriba clavícula: Z (disparo)")
        put("Manos cerca de rodillas:         X (salto 60% altura)")
        put("Palmas tocándose (3s):           Volver al menú")
        
        # Mostrar estado de teclas presionadas
        y += 10
        keys_status = f"Teclas activas: L:{self.keys_pressed['left']} R:{self.keys_pressed['right']}"
        put(keys_status, (200, 200, 0))
        
        # Mostrar estado actual del gesto de pose si está disponible
        if pose_detector:
            pose_action, pose_description = pose_detector.get_current_pose_info()
            
            # Espacio separador
            y += 20
            put("--- ESTADO ACTUAL ---", (100, 100, 255))
            
            # Color según el tipo de gesto
            if pose_action == "ninguna":
                color = (255, 255, 255)  # Blanco - esperando
            elif "inclinacion" in pose_action:
                color = (0, 255, 0)  # Verde - movimiento
            elif pose_action == "salto":
                color = (255, 255, 0)  # Amarillo - salto
            elif pose_action == "brazo_arriba":
                color = (255, 0, 255)  # Magenta - ataque
            elif pose_action == "palmas_tocandose":
                color = (0, 255, 255)  # Cian - menú
            else:
                color = (255, 255, 255)  # Blanco por defecto
            
            put(f"Gesto: {pose_action}", color)
            put(f"Estado: {pose_description}", color)
        
        return frame
