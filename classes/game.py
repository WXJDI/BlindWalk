import pygame
import sys
from settings import *
from classes.player import Player
from classes.obstacle import Obstacle

class Game:
    def __init__(self):
        # Initialisation de Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Instanciation des objets (Création)
        self.player = Player()
        # On crée un obstacle test au milieu
        self.obstacle = Obstacle(400, 200, 50, 200)

    def handle_input(self):
        # Gestion des événements (Fermer la fenêtre, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # On appelle la méthode de mouvement du joueur
        self.player.move()

    def update(self):
        # --- Gestion des Collisions ---
        # Si le joueur touche l'obstacle -> Reset immédiat
        if self.player.rect.colliderect(self.obstacle.rect):
            print("Collision ! Retour au départ.")
            self.player.reset()

    def draw(self):
        # 1. On nettoie l'écran (Fond vert)
        self.screen.fill(GREEN_GRASS)

        # 2. On dessine les objets
        self.obstacle.draw(self.screen)
        self.player.draw(self.screen)

        # 3. On affiche le tout
        pygame.display.flip()

    def run(self):
        # La boucle principale du jeu
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()