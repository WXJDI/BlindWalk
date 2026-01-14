# settings.py

# --- Paramètres de l'écran ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Blind Walk - Escape"

# --- Couleurs (R, G, B) ---
# On leur donne des noms clairs pour ne pas se tromper
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED_DANGER = (255, 0, 0)
GREEN_GRASS = (50, 200, 50)
BLUE_PLAYER = (0, 100, 255)
YELLOW_GOAL = (255, 215, 0)  # <-- NOUVEAU : Couleur de la sortie (Or)

# --- Paramètres du Joueur ---
PLAYER_SIZE = 30
PLAYER_SPEED = 4
# On le place en bas au centre (Largeur/2, Hauteur - 50 pixels)
PLAYER_START_POS = (SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT - 50)