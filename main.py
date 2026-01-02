import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre (Largeur, Hauteur)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Blind Walk - Test V1")

# Boucle du jeu
running = True
while running:
    # Si on clique sur la croix, ça ferme
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Remplir l'écran en Bleu pour tester
    screen.fill((0, 0, 255))
    
    # Mettre à jour l'affichage
    pygame.display.flip()

pygame.quit()
sys.exit()