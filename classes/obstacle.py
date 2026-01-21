import pygame
from settings import *

class Obstacle:
    def __init__(self, x, y, width, height):
        self.image = pygame.Surface((width, height))
        self.image.fill(COLOR_TRAP_A) 
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)