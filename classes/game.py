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
        

        self.game_state = "MENU" 
        self.game_over = False
        self.level_count = 0 
        self.max_levels = 3  
        
        self.font_retro_title = pygame.font.SysFont("Courier New", 50, bold=True)
        self.font_retro_text = pygame.font.SysFont("Courier New", 18, bold=True) 
        self.font_retro_btn = pygame.font.SysFont("Courier New", 30, bold=True)
        self.font_retro_msg = pygame.font.SysFont("Courier New", 14, bold=False, italic=True)
        
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self.game_over_font = pygame.font.SysFont("Arial", 64, bold=True)
        
        self.background_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.load_background()
        self.play_music()

        try:
            heart_path = os.path.join('assets', 'images', 'tiles', 'heart.png')
            flag_path = os.path.join('assets', 'images', 'tiles', 'flag.png')
            self.heart_img = pygame.image.load(heart_path).convert_alpha()
            self.flag_img = pygame.image.load(flag_path).convert_alpha()
        except FileNotFoundError:
            print("ERREUR : Manque heart.png ou flag.png")
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
        self.start_btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 100, 200, 50)

        # Jeu
        self.player = Player()
        self.traps_a = []
        self.traps_b = []
        self.traps_c = []

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
        
        nb_traps = 10 + (self.level_count * 2) 

        for _ in range(nb_traps):
            x = random.randint(0, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 100)
            self.traps_a.append(Obstacle(x, y, random.randint(30, 60), random.randint(30, 60)))

        for _ in range(nb_traps):
            x = random.randint(0, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 100)
            self.traps_b.append(Stone(x, y, random.randint(30, 60), random.randint(30, 60)))

        for _ in range(nb_traps):
            x = random.randint(0, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 100)
            self.traps_c.append(Mud(x, y, random.randint(30, 60), random.randint(30, 60)))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    
            if self.game_state == "VICTORY":
                if event.type == pygame.KEYDOWN:
                    
                    self.game_state = "MENU"
                    self.level_count = 0
                return

            # --- MENU ---
            if self.game_state == "MENU":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.start_btn_rect.collidepoint(event.pos):
                        self.start_game()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.start_game()
                return

            # --- JEU ---
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

    def start_game(self):
        self.game_state = "PLAYING"
        self.level_count = 0
        self.player.reset()
        self.create_map()

    def update(self):
        if self.game_state != "PLAYING": return
        if self.game_over: return

        if self.player.rect.colliderect(self.goal_hitbox):
            print("NIVEAU GAGNÉ !")
            self.level_count += 1
            
            if self.level_count >= self.max_levels:
                self.game_state = "VICTORY"
            else:
                self.player.reset()
                self.create_map()
                
        all_traps = self.traps_a + self.traps_b + self.traps_c
        for trap in all_traps:
            if self.player.rect.colliderect(trap.rect):
                self.game_over = True
                break

    def draw_victory(self):
        self.screen.fill(BLACK)
        
        title = self.font_retro_title.render("MISSION ACCOMPLIE !", True, (255, 215, 0)) # Or
        rect_title = title.get_rect(center=(SCREEN_WIDTH//2, 80))
        self.screen.blit(title, rect_title)
        
        messages = [
            "Bravo. Vous avez réussi à vous adapter.",
            "Vous avez utilisé des filtres pour contourner les obstacles.",
            "",
            "MAIS SOUVENEZ-VOUS :",
            "Dans la vraie vie, on ne peut pas changer de filtre.",
            "Le daltonisme et la malvoyance ne sont pas des options.",
            "Ils sont vécus chaque jour, sans bouton 'Pause' ou 'Reset'.",
            "",
            "Soyons attentifs. Construisons un monde plus inclusif.",
            "Où le danger n'est invisible pour personne.",
        ]
        
        start_y = 160
        for i, line in enumerate(messages):
            col = (0, 255, 255) if i > 3 else WHITE
            
            text = self.font_retro_text.render(line, True, col)
            rect = text.get_rect(center=(SCREEN_WIDTH//2, start_y))
            self.screen.blit(text, rect)
            start_y += 35

        txt_quit = self.font_retro_btn.render("[APPUYEZ SUR UNE TOUCHE]", True, GRAY_TEXT)
        rect_quit = txt_quit.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        self.screen.blit(txt_quit, rect_quit)

        pygame.display.flip()

    def draw_menu(self):
        self.screen.fill(BLACK)
        title = self.font_retro_title.render("BLIND WALK", True, (0, 255, 0))
        rect_title = title.get_rect(center=(SCREEN_WIDTH//2, 80))
        self.screen.blit(title, rect_title)
        
        instructions = [
            "MISSION : SURVIVRE A 3 NIVEAUX",
            "------------------------------",
            "1. DEUTERANOPIE : Cache les pièges ROUGES",
            "2. TRITANOPIE   : Cache les pièges BLEUS",
            "3. ACHROMATOPSIE: Cache les pièges ORANGES",
            "",
            "MEMORISEZ LE CHEMIN. CHANGEZ DE VUE.",
        ]
        
        start_y = 160
        for line in instructions:
            text = self.font_retro_text.render(line, True, WHITE)
            rect = text.get_rect(center=(SCREEN_WIDTH//2, start_y))
            self.screen.blit(text, rect)
            start_y += 30

        pygame.draw.rect(self.screen, WHITE, self.start_btn_rect)
        pygame.draw.rect(self.screen, (0, 255, 0), self.start_btn_rect, 3) 
        txt_start = self.font_retro_btn.render("COMMENCER", True, BLACK)
        rect_start = txt_start.get_rect(center=self.start_btn_rect.center)
        self.screen.blit(txt_start, rect_start)

        message = "SAVIEZ-VOUS QUE 300 MILLIONS DE PERSONNES NE VOIENT PAS LE DANGER COMME VOUS ?"
        txt_msg = self.font_retro_msg.render(message, True, (0, 255, 255))
        rect_msg = txt_msg.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
        self.screen.blit(txt_msg, rect_msg)

        pygame.display.flip()

    def draw(self):
        if self.game_state == "MENU":
            self.draw_menu()
            return
        
        if self.game_state == "VICTORY":
            self.draw_victory()
            return

        palette = FILTERS[self.current_filter]
        
        self.screen.fill(palette["bg"])
        self.screen.blit(self.background_surf, (0, 0), special_flags=pygame.BLEND_MULT)
        
        self.screen.blit(self.flag_img, self.flag1_pos)
        self.screen.blit(self.heart_img, self.heart_pos)
        flag_flipped = pygame.transform.flip(self.flag_img, True, False)
        self.screen.blit(flag_flipped, self.flag2_pos)
        
        lvl_txt = self.font.render(f"NIVEAU {self.level_count + 1} / {self.max_levels}", True, WHITE)
        self.screen.blit(lvl_txt, (10, 10))

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