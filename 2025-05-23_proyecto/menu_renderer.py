import cv2

class MenuRenderer:
    def __init__(self):
        self.games = ["Juego del Dinosaurio", "Juego del Laberinto", "Hollow Knight"]

        self.selected_index = 0
        
        
    def navigate_up(self):
        """Navega hacia arriba en el menú"""
        self.selected_index = (self.selected_index - 1) % len(self.games)
        print(f"Menú: Seleccionado {self.games[self.selected_index]}")
        
    def navigate_down(self):
        """Navega hacia abajo en el menú"""
        self.selected_index = (self.selected_index + 1) % len(self.games)
        print(f"Menú: Seleccionado {self.games[self.selected_index]}")
        
    def draw_menu(self, frame):
        """Dibuja el menú principal sobre el frame de video"""
        # Obtener dimensiones del frame
        height, width = frame.shape[:2]
        
        # Calcular márgenes proporcionales (15% del ancho y alto)
        margin_x = int(width * 0.15)
        margin_y = int(height * 0.1)
        
        # Crear overlay semi-transparente con márgenes apropiados
        overlay = frame.copy()
        cv2.rectangle(overlay, (margin_x, margin_y), 
                     (width - margin_x, height - margin_y), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
        
        # Calcular posiciones de texto basadas en el tamaño del frame
        title_x = margin_x + 40
        title_y = margin_y + 60
        
        # Título del menú - más pequeño
        cv2.putText(frame, "MENU DE JUEGOS POR GESTOS", (title_x, title_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        
        # Instrucciones principales
        controls_y = title_y + 45
        cv2.putText(frame, "Controles:", (title_x, controls_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 255, 150), 1)
        
        # Espaciado más amplio para las instrucciones
        instruction_x = title_x + 30
        line_spacing = 28
        current_y = controls_y + 35
        
        # Navegación
        cv2.putText(frame, "Apuntar arriba: Juego anterior", (instruction_x, current_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
        current_y += line_spacing
        
        cv2.putText(frame, "Apuntar abajo: Siguiente juego", (instruction_x, current_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
        current_y += line_spacing
        
        cv2.putText(frame, "Mano abierta: Seleccionar juego", (instruction_x, current_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
        current_y += line_spacing
        
        cv2.putText(frame, "Puno: Sin accion (neutral)", (instruction_x, current_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.45, (150, 150, 150), 1)
        current_y += line_spacing + 10
        
        # Gestos sostenidos
        cv2.putText(frame, "Gestos sostenidos:", (title_x, current_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 150, 150), 1)
        current_y += 32
        
        cv2.putText(frame, "Signo de paz (1.2s): Ir al juego seleccionado", (instruction_x, current_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
        current_y += line_spacing
        
        cv2.putText(frame, "Signo rock (2s): Cerrar programa", (instruction_x, current_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
        current_y += line_spacing + 18
        
        # Lista de juegos
        cv2.putText(frame, "Juegos disponibles:", (title_x, current_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        current_y += 35
        
        # Renderizar juegos con mejor espaciado
        for i, game in enumerate(self.games):
            color = (0, 255, 0) if i == self.selected_index else (255, 255, 255)
            prefix = "→ " if i == self.selected_index else "  "
            cv2.putText(frame, f"{prefix}{game}", (instruction_x, current_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            current_y += 28
        
        return frame
    
    def get_selected_game(self):
        """Retorna el juego seleccionado actualmente"""
        return self.selected_index
