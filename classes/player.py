import pygame
from settings import *

class Player:
    def __init__(self):
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(COLOR_PLAYER)
        
        # Position de départ
        self.rect = self.image.get_rect(topleft=PLAYER_START_POS)
        self.start_pos = PLAYER_START_POS

    def move(self):
        # Récupérer l'état de toutes les touches
        keys = pygame.key.get_pressed()
        
        # GAUCHE : Flèche Gauche OU Touche Q
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.rect.x -= PLAYER_SPEED
            
        # DROITE : Flèche Droite OU Touche D
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
            
        # HAUT (Avancer) : Flèche Haut OU Touche Z
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.rect.y -= PLAYER_SPEED
            
        # BAS (Reculer) : Flèche Bas OU Touche S
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += PLAYER_SPEED
            
        # Garde-fou (Clamp) pour rester dans l'écran
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def reset(self):
        self.rect.topleft = self.start_pos