import pygame
from settings import * 

class Player:
    def __init__(self):
        # On utilise les constantes de settings.py
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(COLOR_PLAYER)
        
        # Le Rect gère la position et les collisions
        # On déballe le tuple (x, y) de la position de départ
        self.rect = self.image.get_rect(topleft=PLAYER_START_POS)
        
        # Position initiale sauvegardée pour le Reset
        self.start_pos = PLAYER_START_POS

    def move(self):
        # Gestion des touches
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED
            
        # (Bonus Clean Code) Garde-fou pour rester dans l'écran
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def reset(self):
        # Retour à la case départ
        self.rect.topleft = self.start_pos