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
        
        # --- NOUVEAU : Gestion des filtres ---
        self.current_filter = 0 # 0 = Normal par défaut
        self.font = pygame.font.SysFont("Arial", 20) # Police pour l'UI

        self.player = Player()
        self.goal = pygame.Rect(SCREEN_WIDTH // 2 - 50, 0, 100, 20)
        self.obstacles = []
        self.create_map()
        # --- UI CONFIGURATION ---
        self.font = pygame.font.SysFont("Arial", 20)
        self.current_filter = 0
        
        # Création des zones cliquables (Boutons)
        self.buttons = []
        options = [(0, "1: Normal"), (1, "2: Protanope"), (2, "3: Gris")]
        
        offset_x = 10
        y_pos = SCREEN_HEIGHT - 30
        
        for mode_id, text_str in options:
            # 1. On calcule la taille que prendra le texte
            text_surf = self.font.render(text_str, True, WHITE)
            w, h = text_surf.get_size()
            
            # 2. On crée un Rectangle invisible à cet endroit
            rect = pygame.Rect(offset_x, y_pos, w, h)
            
            # 3. On stocke les infos du bouton
            self.buttons.append({
                "rect": rect,
                "text": text_str,
                "id": mode_id
            })
            
            # 4. On décale le x pour le prochain bouton
            offset_x += 130

    def create_map(self):
        # On garde ta logique de création de carte
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
            
            # --- NOUVEAU : Changement de filtre avec 1, 2, 3 ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.current_filter = 0 # Normal
                elif event.key == pygame.K_2:
                    self.current_filter = 1 # Protanopie (Danger !)
                elif event.key == pygame.K_3:
                    self.current_filter = 2 # Gris

        self.player.move()

    def update(self):
        # Logique de collision (inchangée)
        if self.player.rect.colliderect(self.goal):
            print("GAGNÉ !")
            self.player.reset()
            self.create_map() # On recrée une carte pour changer

        for obstacle in self.obstacles:
            if self.player.rect.colliderect(obstacle.rect):
                print("PERDU !")
                self.player.reset()
                break

    def draw_ui(self):
        # --- NOUVEAU : Interface en bas à gauche ---
        # On dessine 3 petits textes
        ui_y = SCREEN_HEIGHT - 30
        
        texts = [
            (0, "1: Normal"),
            (1, "2: Protanope"),
            (2, "3: Gris")
        ]
        
        offset_x = 10
        for mode_id, text_str in texts:
            # Si c'est le mode actif, on l'écrit en Blanc, sinon en Gris
            color = WHITE if self.current_filter == mode_id else (100, 100, 100)
            
            text_surf = self.font.render(text_str, True, color)
            self.screen.blit(text_surf, (offset_x, ui_y))
            
            offset_x += 120 # On décale le prochain texte vers la droite

    def draw(self):
        # 1. Récupérer la palette de couleurs active
        palette = FILTERS[self.current_filter]

        # 2. Dessiner le fond avec la couleur de la palette
        self.screen.fill(palette["bg"])

        # 3. Dessiner la Sortie
        pygame.draw.rect(self.screen, palette["goal"], self.goal)

        # 4. Dessiner les Obstacles (avec la couleur piégée !)
        # Attention : On change la couleur de l'obstacle dynamiquement
        for obstacle in self.obstacles:
            # On crée une surface temporaire pour dessiner l'obstacle
            pygame.draw.rect(self.screen, palette["obstacle"], obstacle.rect)

        # 5. Dessiner le Joueur
        pygame.draw.rect(self.screen, palette["player"], self.player.rect)

        # 6. Dessiner l'interface
        self.draw_ui()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()
        
        
    def handle_input(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # --- GESTION SOURIS (NOUVEAU) ---
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # 1 = Clic Gauche
                        mouse_pos = event.pos # Où a-t-on cliqué ?
                        
                        # On vérifie si la souris touche un de nos boutons
                        for btn in self.buttons:
                            if btn["rect"].collidepoint(mouse_pos):
                                self.current_filter = btn["id"]
                                print(f"Clic ! Mode changé vers : {btn['text']}")

                # (Tu peux garder les touches clavier 1, 2, 3 si tu veux, c'est toujours pratique)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1: self.current_filter = 0
                    elif event.key == pygame.K_2: self.current_filter = 1
                    elif event.key == pygame.K_3: self.current_filter = 2
            
            self.player.move()
            
    def draw_ui(self):
            for btn in self.buttons:
                # Couleur : Blanc si actif, Gris foncé si inactif
                if self.current_filter == btn["id"]:
                    color = WHITE
                else:
                    color = (100, 100, 100) # Gris
                
                # 1. Dessiner le texte
                text_surf = self.font.render(btn["text"], True, color)
                self.screen.blit(text_surf, btn["rect"])
                
                # 2. (Optionnel) Dessiner un petit cadre autour pour bien voir la zone cliquable
                pygame.draw.rect(self.screen, color, btn["rect"], 1) # 1 = épaisseur du trait