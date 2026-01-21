import pygame
import os # 
from settings import *

class Player:
    def __init__(self):

        

        image_path = os.path.join('assets', 'images', 'player', 'player.png')
        
        try:

            self.image = pygame.image.load(image_path).convert_alpha()
            

            self.image = pygame.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))
            
        except FileNotFoundError:
            print(f"ERREUR: Image non trouvée à {image_path}. Utilisation du carré bleu.")
            self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
            self.image.fill(COLOR_PLAYER)

        self.rect = self.image.get_rect(topleft=PLAYER_START_POS)
        self.start_pos = PLAYER_START_POS

    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += PLAYER_SPEED
            
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def reset(self):
        self.rect.topleft = self.start_pos