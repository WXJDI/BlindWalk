# settings.py

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Blind Walk - Cecite Selective"

# --- COULEURS DE BASE ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY_TEXT = (180, 180, 180)

# --- COULEURS DU JEU (Mode Normal) ---
# 1. Le Sol (Vert Olive / Camouflage)
COLOR_BG_NORMAL = (128, 128, 0)      # Olive

# 2. Piège A (Invisible en Deutéranopie) -> Rouge Tomate
COLOR_TRAP_A = (255, 99, 71)

# 3. Piège B (Invisible en Tritanopie) -> Bleu Roi
COLOR_TRAP_B = (65, 105, 225)

# 4. Piège C (Invisible en Achromatopsie) -> Orange (Iso-luminant avec l'Olive)
# En gris, (128,128,0) donne ~112. (255, 140, 0) donne ~140.
# On trichera dans le filtre Gris pour les forcer à la même valeur exacte.
COLOR_TRAP_C = (255, 140, 0) 

COLOR_GOAL = (255, 215, 0)     # Or
COLOR_PLAYER = (255, 255, 255) # Blanc pur (Toujours visible)


# --- LES LUNETTES (PALETTES) ---
FILTERS = {
    0: { 
        "name": "Deuteranopie (Vert/Rouge)",
        # Le Rouge (Trap A) devient comme le fond -> INVISIBLE
        "bg": (160, 150, 60),           
        "trap_a": (160, 150, 60), # Camouflé
        "trap_b": (80, 100, 180), # Visible
        "trap_c": (180, 140, 60), # Visible
        "goal": (220, 220, 100),
        "player": (240, 240, 240)
    },
    
    1: { 
        "name": "Tritanopie (Bleu/Jaune)",
        # Le Bleu (Trap B) devient comme le fond -> INVISIBLE
        "bg": (100, 130, 130),            
        "trap_a": (255, 110, 110), # Visible
        "trap_b": (100, 130, 130), # Camouflé
        "trap_c": (200, 120, 120), # Visible
        "goal": (200, 160, 160),
        "player": (240, 240, 240)
    },
    
    2: { 
        "name": "Achromatopsie (Formes)",
        # L'Orange (Trap C) a la même luminosité que le fond -> INVISIBLE
        "bg": (115, 115, 115),     
        "trap_a": (150, 150, 150), # Visible
        "trap_b": (80, 80, 80),    # Visible
        "trap_c": (115, 115, 115), # Camouflé
        "goal": (220, 220, 220),
        "player": (255, 255, 255)
    }
}

# Paramètres Joueur
PLAYER_SIZE = 30
PLAYER_SPEED = 4
PLAYER_START_POS = (SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT - 50)