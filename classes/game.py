import pygame
import sys
import os
import random
from settings import *
from classes.player import Player
from classes.obstacle import Obstacle
from classes.stone import Stone
from classes.mud import Mud

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # --- ETAT DU JEU ---
        # "MENU" = L'écran d'accueil
        # "PLAYING" = Le jeu commence
        self.game_state = "MENU" 
        self.game_over = False
        
        # --- POLICES RETRO ---
        # "Courier New" donne un look machine à écrire / terminal très rétro
        self.font_retro_title = pygame.font.SysFont("Courier New", 50, bold=True)
        self.font_retro_text = pygame.font.SysFont("Courier New", 20, bold=True)
        self.font_retro_btn = pygame.font.SysFont("Courier New", 30, bold=True)
        self.font_retro_msg = pygame.font.SysFont("Courier New", 14, bold=False, italic=True)
        
        # UI Jeu (Garder l'ancienne police pour l'interface en bas)
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self.game_over_font = pygame.font.SysFont("Arial", 64, bold=True)
        
        # --- CHARGEMENT DU BACKGROUND ---
        self.background_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.load_background()
        
        # --- CHARGEMENT MUSIQUE ---
        self.play_music()

        # --- IMAGES VICTOIRE ---
        try:
            heart_path = os.path.join('assets', 'images', 'tiles', 'heart.png')
            flag_path = os.path.join('assets', 'images', 'tiles', 'flag.png')
            self.heart_img = pygame.image.load(heart_path).convert_alpha()
            self.flag_img = pygame.image.load(flag_path).convert_alpha()
        except FileNotFoundError:
            print("ERREUR CRITIQUE : Images de victoire manquantes.")
            sys.exit()

        # Calcul positions victoire
        h_w, h_h = self.heart_img.get_size()
        f_w, f_h = self.flag_img.get_size()
        spacing = 10
        total_goal_width = f_w + spacing + h_w + spacing + f_w
        start_x = (SCREEN_WIDTH - total_goal_width) // 2
        y_pos = 5
        self.flag1_pos = (start_x, y_pos)
        self.heart_pos = (start_x + f_w + spacing, y_pos)
        self.flag2_pos = (start_x + f_w + spacing + h_w + spacing, y_pos)
        max_h = max(h_h, f_h)
        self.goal_hitbox = pygame.Rect(start_x, y_pos, total_goal_width, max_h)
        
        # --- BOUTONS INTERFACE ---
        self.current_filter = 0
        self.buttons = []
        self.create_ui_buttons()
        
        # --- BOUTON START DU MENU ---
        # On crée un rectangle pour le bouton "START"
        self.start_btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 100, 200, 50)

        # Jeu
        self.player = Player()
        self.traps_a = []
        self.traps_b = []
        self.traps_c = []
        self.create_map()

    def load_background(self):
        try:
            grass_path = os.path.join('assets', 'images', 'tiles', 'grass.png')
            grass_img = pygame.image.load(grass_path).convert()
        except FileNotFoundError:
            return

        tile_w = grass_img.get_width()
        tile_h = grass_img.get_height()
        for y in range(0, SCREEN_HEIGHT, tile_h):
            for x in range(0, SCREEN_WIDTH, tile_w):
                self.background_surf.blit(grass_img, (x, y))
        self.background_surf = pygame.transform.grayscale(self.background_surf)

    def play_music(self):
        music_path = os.path.join('assets', 'sounds', 'music.mp3')
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

    def create_ui_buttons(self):
        options = [
            (0, "1: Deuteranopie"), 
            (1, "2: Tritanopie"), 
            (2, "3: Achromatopsie")
        ]
        start_x = (SCREEN_WIDTH - 600) // 2
        offset_x = 20
        y_pos = SCREEN_HEIGHT - 40
        self.buttons = []
        for mode_id, text_str in options:
            text_surf = self.font.render(text_str, True, WHITE)
            w, h = text_surf.get_size()
            rect = pygame.Rect(offset_x, y_pos, w + 10, h + 10)
            self.buttons.append({"rect": rect, "text": text_str, "id": mode_id})
            offset_x += w + 40

    def create_map(self):
        self.traps_a = []
        self.traps_b = []
        self.traps_c = []
        
        for _ in range(10):
            x = random.randint(0, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 100)
            self.traps_a.append(Obstacle(x, y, random.randint(30, 60), random.randint(30, 60)))

        for _ in range(10):
            x = random.randint(0, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 100)
            self.traps_b.append(Stone(x, y, random.randint(30, 60), random.randint(30, 60)))

        for _ in range(10):
            x = random.randint(0, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 100)
            self.traps_c.append(Mud(x, y, random.randint(30, 60), random.randint(30, 60)))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # --- GESTION DU MENU D'ACCUEIL ---
            if self.game_state == "MENU":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Si on clique sur le bouton START
                    if self.start_btn_rect.collidepoint(event.pos):
                        self.game_state = "PLAYING" # On lance le jeu !
                
                # Optionnel : Appuyer sur ENTRÉE pour commencer aussi
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.game_state = "PLAYING"
                
                return # On arrête la lecture des inputs ici si on est dans le menu

            # --- GESTION EN JEU ---
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

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in self.buttons:
                    if btn["rect"].collidepoint(event.pos):
                        self.current_filter = btn["id"]

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: self.current_filter = 0
                elif event.key == pygame.K_2: self.current_filter = 1
                elif event.key == pygame.K_3: self.current_filter = 2

        if self.game_state == "PLAYING" and not self.game_over:
            self.player.move()

    def update(self):
        if self.game_state == "MENU": return # Rien ne bouge dans le menu
        if self.game_over: return

        if self.player.rect.colliderect(self.goal_hitbox):
            print("GAGNÉ !")
            self.player.reset()
            self.create_map()

        # Collisions pièges
        all_traps = self.traps_a + self.traps_b + self.traps_c
        for trap in all_traps:
            if self.player.rect.colliderect(trap.rect):
                self.game_over = True
                break

    # --- NOUVELLE FONCTION : DESSINER LE MENU ---
    def draw_menu(self):
        # 1. Fond noir retro
        self.screen.fill(BLACK)
        
        # 2. Titre du jeu
        title = self.font_retro_title.render("BLIND WALK", True, (0, 255, 0)) # Vert Hacker
        rect_title = title.get_rect(center=(SCREEN_WIDTH//2, 80))
        self.screen.blit(title, rect_title)
        
        # 3. Les instructions (Règles du jeu)
        instructions = [
            "MISSION : ATTEINDRE LE DRAPEAU",
            "------------------------------",
            "1. DEUTERANOPIE : Cache les pièges ROUGES",
            "2. TRITANOPIE   : Cache les pièges BLEUS",
            "3. ACHROMATOPSIE: Cache les pièges ORANGES",
            "",
            "MEMORISEZ LE CHEMIN. CHANGEZ DE VUE. SURVIVEZ.",
        ]
        
        start_y = 160
        for line in instructions:
            text = self.font_retro_text.render(line, True, WHITE)
            rect = text.get_rect(center=(SCREEN_WIDTH//2, start_y))
            self.screen.blit(text, rect)
            start_y += 30

        # 4. Le Bouton START
        pygame.draw.rect(self.screen, WHITE, self.start_btn_rect)
        pygame.draw.rect(self.screen, (0, 255, 0), self.start_btn_rect, 3) 
        
        txt_start = self.font_retro_btn.render("COMMENCER", True, BLACK)
        rect_start = txt_start.get_rect(center=self.start_btn_rect.center)
        self.screen.blit(txt_start, rect_start)

        # --- 5. LE MESSAGE DE SENSIBILISATION (NOUVEAU) ---
        # On définit le texte (Tu peux le changer ici)
        message = "SAVIEZ-VOUS QUE 300 MILLIONS DE PERSONNES NE VOIENT PAS LE DANGER COMME VOUS ?"
        
        # On crée le rendu (en Cyan pour faire sérieux/médical)
        txt_msg = self.font_retro_msg.render(message, True, (0, 255, 255))
        rect_msg = txt_msg.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
        
        # On l'affiche
        self.screen.blit(txt_msg, rect_msg)
        # --------------------------------------------------

        pygame.display.flip()

    def draw(self):
        # SI ON EST DANS LE MENU, ON DESSINE LE MENU ET ON S'ARRETE LA
        if self.game_state == "MENU":
            self.draw_menu()
            return

        # SINON ON DESSINE LE JEU NORMAL
        palette = FILTERS[self.current_filter]
        
        self.screen.fill(palette["bg"])
        self.screen.blit(self.background_surf, (0, 0), special_flags=pygame.BLEND_MULT)
        
        # Objectifs
        self.screen.blit(self.flag_img, self.flag1_pos)
        self.screen.blit(self.heart_img, self.heart_pos)
        flag_flipped = pygame.transform.flip(self.flag_img, True, False)
        self.screen.blit(flag_flipped, self.flag2_pos)
        
        # Pièges
        show_outline = (self.current_filter == 2)

        if self.current_filter != 0: 
            for trap in self.traps_a:
                pygame.draw.rect(self.screen, palette["trap_a"], trap.rect)
                if show_outline: pygame.draw.rect(self.screen, BLACK, trap.rect, 1)

        if self.current_filter != 1:
            for trap in self.traps_b:
                pygame.draw.rect(self.screen, palette["trap_b"], trap.rect)
                if show_outline: pygame.draw.rect(self.screen, BLACK, trap.rect, 1)

        if self.current_filter != 2:
            for trap in self.traps_c:
                pygame.draw.rect(self.screen, palette["trap_c"], trap.rect)

        self.player.draw(self.screen)
        self.draw_ui()

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def draw_ui(self):
        menu_bg = pygame.Surface((SCREEN_WIDTH, 50))
        menu_bg.set_alpha(100)
        menu_bg.fill(BLACK)
        self.screen.blit(menu_bg, (0, SCREEN_HEIGHT - 50))

        for btn in self.buttons:
            color = WHITE if self.current_filter == btn["id"] else GRAY_TEXT
            text_surf = self.font.render(btn["text"], True, color)
            text_rect = text_surf.get_rect(center=btn["rect"].center)
            self.screen.blit(text_surf, text_rect)
            if self.current_filter == btn["id"]:
                pygame.draw.rect(self.screen, WHITE, btn["rect"], 1)

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        col = COLOR_TRAP_A
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