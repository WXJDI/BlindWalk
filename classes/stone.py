import pygame
from settings import *

class Stone:
    def __init__(self, x, y, width, height):
        self.image = pygame.Surface((width, height))
        # Piège Bleu
        self.image.fill(COLOR_TRAP_B) 
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)