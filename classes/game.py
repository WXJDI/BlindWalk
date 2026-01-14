import pygame
import sys
import random
from settings import *
from classes.player import Player
from classes.obstacle import Obstacle

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # --- ETAT DU JEU ---
        self.game_over = False  # Nouvelle variable pour savoir si on a perdu
        
        # UI & Fontes
        self.font = pygame.font.SysFont("Arial", 20)
        self.game_over_font = pygame.font.SysFont("Arial", 64, bold=True)
        
        # Filtres
        self.current_filter = 0
        self.buttons = []
        self.create_ui_buttons()

        # Objets du jeu
        self.player = Player()
        self.goal = pygame.Rect(SCREEN_WIDTH // 2 - 50, 0, 100, 20)
        self.obstacles = []
        self.create_map()

    def create_ui_buttons(self):
        # Création des boutons de filtre (comme vu précédemment)
        options = [(0, "1: Normal"), (1, "2: Protanope"), (2, "3: Gris")]
        offset_x = 10
        y_pos = SCREEN_HEIGHT - 30
        
        for mode_id, text_str in options:
            text_surf = self.font.render(text_str, True, WHITE)
            w, h = text_surf.get_size()
            rect = pygame.Rect(offset_x, y_pos, w, h)
            self.buttons.append({"rect": rect, "text": text_str, "id": mode_id})
            offset_x += 130

    def create_map(self):
        self.obstacles = []
        for _ in range(15):
            x = random.randint(0, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 100)
            w = random.randint(30, 80)
            h = random.randint(30, 80)
            self.obstacles.append(Obstacle(x, y, w, h))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # --- INPUTS SI GAME OVER ---
            if self.game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    # Touche R pour recommencer
                    self.game_over = False
                    self.player.reset()
                    self.create_map() # Nouvelle carte
                continue # On ignore les autres touches si on est mort

            # --- INPUTS NORMAUX (Jeu en cours) ---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in self.buttons:
                    if btn["rect"].collidepoint(event.pos):
                        self.current_filter = btn["id"]

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: self.current_filter = 0
                elif event.key == pygame.K_2: self.current_filter = 1
                elif event.key == pygame.K_3: self.current_filter = 2

        # Le joueur ne bouge que si le jeu n'est PAS fini
        if not self.game_over:
            self.player.move()

    def update(self):
        if self.game_over:
            return # On ne calcule rien si le jeu est fini

        # Victoire
        if self.player.rect.colliderect(self.goal):
            print("GAGNÉ !")
            self.player.reset()
            self.create_map()

        # Défaite (Game Over)
        for obstacle in self.obstacles:
            if self.player.rect.colliderect(obstacle.rect):
                print("GAME OVER !")
                self.game_over = True # <--- C'est ici que tout s'arrête
                # On ne reset PAS le joueur, on fige le jeu

    def draw_ui(self):
        for btn in self.buttons:
            color = WHITE if self.current_filter == btn["id"] else (100, 100, 100)
            text_surf = self.font.render(btn["text"], True, color)
            self.screen.blit(text_surf, btn["rect"])

    def draw_game_over(self):
        # Affiche un écran sombre transparent
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180) # Transparence
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Texte GAME OVER
        text = self.game_over_font.render("GAME OVER", True, RED_DANGER)
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20))
        self.screen.blit(text, rect)
        
        # Texte "Rejouer"
        retry_text = self.font.render("Appuie sur 'R' pour recommencer", True, WHITE)
        retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
        self.screen.blit(retry_text, retry_rect)

    def draw(self):
        palette = FILTERS[self.current_filter]
        
        # Dessin du jeu normal
        self.screen.fill(palette["bg"])
        pygame.draw.rect(self.screen, palette["goal"], self.goal)
        
        for obstacle in self.obstacles:
            # On utilise la couleur dynamique du filtre
            pygame.draw.rect(self.screen, palette["obstacle"], obstacle.rect)
            
        pygame.draw.rect(self.screen, palette["player"], self.player.rect)
        self.draw_ui()

        # Si Game Over, on dessine l'écran de fin PAR DESSUS
        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()