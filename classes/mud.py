import pygame
from settings import *

class Mud:
    def __init__(self, x, y, width, height):
        self.image = pygame.Surface((width, height))
        # Piège Iso-luminant (Orange)
        self.image.fill(COLOR_TRAP_C) 
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)