import pygame
import sys
import os # <--- TRES IMPORTANT ne l'oublie pas
import random
from settings import *
from classes.player import Player
from classes.obstacle import Obstacle
from classes.stone import Stone
from classes.mud import Mud

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self.game_over_font = pygame.font.SysFont("Arial", 64, bold=True)
        
        # --- PREPARATION DU BACKGROUND (NOUVEAU) ---
        self.background_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.load_background() # On appelle la fonction de chargement
        
        # UI
        self.current_filter = 0
        self.buttons = []
        self.create_ui_buttons()

        # Jeu
        self.player = Player()
        self.goal = pygame.Rect(SCREEN_WIDTH // 2 - 50, 0, 100, 20)
        
        self.traps_a = []
        self.traps_b = []
        self.traps_c = []
        
        self.create_map()

    def load_background(self):
        # 1. Charger l'image de l'herbe
        try:
            grass_path = os.path.join('assets', 'images', 'tiles', 'grass.png')
            grass_img = pygame.image.load(grass_path).convert()
        except FileNotFoundError:
            print("Erreur: Image grass.png introuvable. Fond noir par défaut.")
            return

        # 2. Remplir une grande surface avec cette tuile (Tiling)
        # On boucle pour coller l'image partout sur l'écran (800x600)
        tile_w = grass_img.get_width()
        tile_h = grass_img.get_height()
        
        for y in range(0, SCREEN_HEIGHT, tile_h):
            for x in range(0, SCREEN_WIDTH, tile_w):
                self.background_surf.blit(grass_img, (x, y))
        
        # 3. Transformer en Niveaux de Gris (Grayscale)
        # C'est l'astuce ! Une image grise prend parfaitement la couleur qu'on lui applique ensuite.
        # (Cette fonction existe depuis Pygame 2.1.4, tu as la 2.6.1 donc c'est bon)
        self.background_surf = pygame.transform.grayscale(self.background_surf)

    def create_ui_buttons(self):
        # On raccourcit les textes pour que ça rentre
        options = [
            (0, "1: Normal"), 
            (1, "2: Deuteranopie"), 
            (2, "3: Tritanopie"), 
            (3, "4: Achromatopsie")
        ]
        
        # Centrage des boutons
        total_width = sum([len(t)*10 for i, t in options]) # estimation
        start_x = (SCREEN_WIDTH - 600) // 2
        offset_x = 20
        y_pos = SCREEN_HEIGHT - 40
        
        self.buttons = []
        for mode_id, text_str in options:
            text_surf = self.font.render(text_str, True, WHITE)
            w, h = text_surf.get_size()
            rect = pygame.Rect(offset_x, y_pos, w + 10, h + 10) # Zone plus large
            self.buttons.append({"rect": rect, "text": text_str, "id": mode_id})
            offset_x += w + 40

    def create_map(self):
        self.traps_a = []
        self.traps_b = []
        self.traps_c = []
        
        # On génère BEAUCOUP de pièges pour forcer l'utilisation des filtres
        # A. Pièges ROUGES (Invisible Mode 1)
        for _ in range(10):
            x = random.randint(0, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 100)
            self.traps_a.append(Obstacle(x, y, random.randint(30, 60), random.randint(30, 60)))

        # B. Pièges BLEUS (Invisible Mode 2)
        for _ in range(10):
            x = random.randint(0, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 100)
            self.traps_b.append(Stone(x, y, random.randint(30, 60), random.randint(30, 60)))

        # C. Pièges ISO (Invisible Mode 3)
        for _ in range(10):
            x = random.randint(0, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 100)
            self.traps_c.append(Mud(x, y, random.randint(30, 60), random.randint(30, 60)))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game_over = False
                        self.player.reset()
                    elif event.key == pygame.K_n:
                        self.game_over = False
                        self.player.reset()
                        self.create_map()
                continue

            # Clics Souris
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in self.buttons:
                    if btn["rect"].collidepoint(event.pos):
                        self.current_filter = btn["id"]

            # Raccourcis Clavier
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: self.current_filter = 0
                elif event.key == pygame.K_2: self.current_filter = 1
                elif event.key == pygame.K_3: self.current_filter = 2
                elif event.key == pygame.K_4: self.current_filter = 3

        if not self.game_over:
            self.player.move()

    def update(self):
        if self.game_over: return

        if self.player.rect.colliderect(self.goal):
            print("GAGNÉ !")
            self.player.reset()
            self.create_map()

        # TOUS LES PIÈGES SONT MORTELS MAINTENANT
        all_traps = self.traps_a + self.traps_b + self.traps_c
        for trap in all_traps:
            if self.player.rect.colliderect(trap.rect):
                self.game_over = True
                break

    def draw(self):
        palette = FILTERS[self.current_filter]
        
        # 1. Dessin du fond texturé et coloré (Ça c'est parfait, on garde)
        self.screen.fill(palette["bg"])
        self.screen.blit(self.background_surf, (0, 0), special_flags=pygame.BLEND_MULT)
        
        pygame.draw.rect(self.screen, palette["goal"], self.goal)
        
        # --- LOGIQUE DE CAMOUFLAGE ---
        # Au lieu de juste changer la couleur, on vérifie si le piège doit être visible.
        
        # Mode 3 (Achromatopsie) : On active le contour pour voir les formes
        show_outline = (self.current_filter == 3)

        # 1. Pièges A (ROUGES)
        # Ils sont INVISIBLES si on est en Mode 1 (Deutéranopie)
        if self.current_filter != 1: 
            for trap in self.traps_a:
                pygame.draw.rect(self.screen, palette["trap_a"], trap.rect)
                if show_outline: pygame.draw.rect(self.screen, BLACK, trap.rect, 1)

        # 2. Pièges B (BLEUS)
        # Ils sont INVISIBLES si on est en Mode 2 (Tritanopie)
        if self.current_filter != 2:
            for trap in self.traps_b:
                pygame.draw.rect(self.screen, palette["trap_b"], trap.rect)
                if show_outline: pygame.draw.rect(self.screen, BLACK, trap.rect, 1)

        # 3. Pièges C (ISO-LUMINANTS / ORANGE)
        # Ils sont INVISIBLES si on est en Mode 3 (Achromatopsie)
        # (Car ils ont le même gris que le sol, donc on les cache complètement)
        if self.current_filter != 3:
            for trap in self.traps_c:
                pygame.draw.rect(self.screen, palette["trap_c"], trap.rect)

        # 4. Joueur et Interface
        self.player.draw(self.screen)
        self.draw_ui()

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()
        
    def draw_ui(self):
        # Fond semi-transparent pour le menu du bas
        menu_bg = pygame.Surface((SCREEN_WIDTH, 50))
        menu_bg.set_alpha(100)
        menu_bg.fill(BLACK)
        self.screen.blit(menu_bg, (0, SCREEN_HEIGHT - 50))

        for btn in self.buttons:
            color = WHITE if self.current_filter == btn["id"] else GRAY_TEXT
            text_surf = self.font.render(btn["text"], True, color)
            # Centrer le texte dans le bouton
            text_rect = text_surf.get_rect(center=btn["rect"].center)
            self.screen.blit(text_surf, text_rect)
            
            # Petit cadre si actif
            if self.current_filter == btn["id"]:
                pygame.draw.rect(self.screen, WHITE, btn["rect"], 1)

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        col = COLOR_TRAP_A # Rouge
        text = self.game_over_font.render("GAME OVER", True, col)
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(text, rect)
        
        font_small = pygame.font.SysFont("Arial", 24)
        txt_retry = font_small.render("[R] Réessayer   [N] Nouveau", True, WHITE)
        rect_retry = txt_retry.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
        self.screen.blit(txt_retry, rect_retry)

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()