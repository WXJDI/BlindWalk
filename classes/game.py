import pygame
import sys
import random  # <-- NOUVEAU : Pour l'aléatoire
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

        # 1. Création du Joueur (il va se placer tout seul en bas grâce à settings.py)
        self.player = Player()

        # 2. Création de la Sortie (Un rectangle jaune tout en haut)
        # Rect(x, y, largeur, hauteur) -> Centré en haut
        self.goal = pygame.Rect(SCREEN_WIDTH // 2 - 50, 0, 100, 20)

        # 3. Création des Obstacles "éparpillés"
        self.obstacles = [] # On crée une liste vide
        self.create_map()   # On appelle une fonction pour remplir la liste

    def create_map(self):
        # On va créer 15 obstacles au hasard
        for _ in range(15):
            # x : n'importe où sur la largeur
            x = random.randint(0, SCREEN_WIDTH - 50)
            # y : n'importe où MAIS pas trop près du départ (en bas) ni de l'arrivée (en haut)
            y = random.randint(50, SCREEN_HEIGHT - 100)
            
            # Taille aléatoire pour varier les plaisirs
            w = random.randint(30, 80)
            h = random.randint(30, 80)
            
            # On crée l'objet et on l'ajoute à la liste
            nouvel_obstacle = Obstacle(x, y, w, h)
            self.obstacles.append(nouvel_obstacle)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.player.move()

    def update(self):
        # A. Vérifier collision avec LA SORTIE (Victoire)
        if self.player.rect.colliderect(self.goal):
            print("GAGNÉ ! Tu es sorti du parc !")
            self.player.reset() # On recommence pour l'instant

        # B. Vérifier collision avec LES OBSTACLES (Défaite)
        # On doit vérifier chaque obstacle de la liste un par un
        for obstacle in self.obstacles:
            if self.player.rect.colliderect(obstacle.rect):
                print("Aïe ! Collision avec un obstacle.")
                self.player.reset()
                break # Pas besoin de vérifier les autres si on est mort

    def draw(self):
        self.screen.fill(GREEN_GRASS)

        # 1. Dessiner la sortie
        pygame.draw.rect(self.screen, YELLOW_GOAL, self.goal)

        # 2. Dessiner TOUS les obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # 3. Dessiner le joueur
        self.player.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()