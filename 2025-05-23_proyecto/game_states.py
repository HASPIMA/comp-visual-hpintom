
from enum import Enum

class GameState(Enum):
    MAIN_MENU = "main_menu"
    DINO_GAME = "dino_game"
    LABERINTO_GAME = "laberinto_game"
    HOLLOW_KNIGHT = "hollow_knight"  # ← nuevo
    CLOSED = "closed"