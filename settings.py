# settings.py

# --- Paramètres de l'écran ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Blind Walk - Escape"

# --- Couleurs de base (Utiles pour l'interface ou les tests) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# --- Couleurs Logiques (Mode Normal) ---
COLOR_GRASS = (50, 200, 50)   # Vert
COLOR_TRAP = (255, 0, 0)      # Rouge vif
COLOR_GOAL = (255, 215, 0)    # Or
COLOR_PLAYER = (0, 100, 255)  # Bleu

# --- LA MAGIE DES FILTRES (Palettes de couleurs) ---
# C'est ici que tu règles la difficulté visuelle.
# 0 = Normal, 1 = Protanopie (Piège invisible), 2 = Achromatopsie (Noir et Blanc)

FILTERS = {
    0: { # MODE NORMAL (Tout est clair, contraste fort)
        "name": "Normal",
        "bg": COLOR_GRASS,
        "obstacle": COLOR_TRAP,
        "goal": COLOR_GOAL,
        "player": COLOR_PLAYER
    },
    1: { # MODE PROTANOPIE (Simulation de déficit Rouge/Vert)
        "name": "Protanopie",
        "bg": (180, 160, 50),       # Jaune moutarde (Herbe simulée)
        "obstacle": (180, 160, 50), # EXACTEMENT la même couleur que le fond ! (Le piège disparaît)
        "goal": (200, 190, 60),     # Jaune un peu différent
        "player": (50, 80, 200)     # Le bleu reste visible mais terne
    },
    2: { # MODE ACHROMATOPSIE (Nuances de gris)
        "name": "Gris",
        "bg": (100, 100, 100),      # Gris clair
        "obstacle": (60, 60, 60),   # Gris foncé (Visible par contraste)
        "goal": (220, 220, 220),    # Gris très clair
        "player": (150, 150, 150)
    }
}

# --- Paramètres du Joueur ---
PLAYER_SIZE = 30
PLAYER_SPEED = 4
# Position de départ : Centré en bas de l'écran
PLAYER_START_POS = (SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT - 50)