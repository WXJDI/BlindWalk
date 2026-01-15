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
        "name": "Normal (Yeux Nus)",
        "bg": COLOR_BG_NORMAL,
        "trap_a": COLOR_TRAP_A, # Rouge Tomate
        "trap_b": COLOR_TRAP_B, # Bleu Roi
        "trap_c": COLOR_TRAP_C, # Orange
        "goal": COLOR_GOAL,
        "player": COLOR_PLAYER
    },
    
    1: { 
        "name": "Deuteranopie (Vert/Rouge)",
        # ILLUSION : Le Rouge devient comme le fond (Jaune/Moutarde)
        "bg": (160, 150, 60),           
        "trap_a": (160, 150, 60), # MATCH TOTAL -> INVISIBLE
        "trap_b": (80, 100, 180), # Le Bleu reste foncé -> VISIBLE
        "trap_c": (180, 140, 60), # L'Orange reste différent -> VISIBLE
        "goal": (220, 220, 100),
        "player": (240, 240, 240)
    },
    
    2: { 
        "name": "Tritanopie (Bleu/Jaune)",
        # ILLUSION : Le Bleu devient comme le fond (Turquoise sombre)
        "bg": (100, 130, 130),            
        "trap_a": (255, 110, 110), # Le Rouge devient Rose vif -> TRES VISIBLE
        "trap_b": (100, 130, 130), # MATCH TOTAL -> INVISIBLE
        "trap_c": (200, 120, 120), # L'Orange devient Rose saumon -> VISIBLE
        "goal": (200, 160, 160),
        "player": (240, 240, 240)
    },
    
    3: { 
        "name": "Achromatopsie (Formes)",
        # ILLUSION : Iso-luminance. Piège C a le même gris que le sol.
        "bg": (115, 115, 115),     # Gris Moyen
        "trap_a": (150, 150, 150), # Gris Clair (Visible)
        "trap_b": (80, 80, 80),    # Gris Foncé (Visible)
        "trap_c": (115, 115, 115), # MATCH TOTAL -> INVISIBLE
        "goal": (220, 220, 220),
        "player": (255, 255, 255)
    }
}

# Paramètres Joueur
PLAYER_SIZE = 30
PLAYER_SPEED = 4
PLAYER_START_POS = (SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT - 50)