import pygame
import os # <--- NOUVEAU : Nécessaire pour gérer les chemins de fichiers
from settings import *

class Player:
    def __init__(self):
        # --- NOUVELLE MÉTHODE POUR CHARGER L'IMAGE ---
        
        # 1. On construit le chemin vers le fichier image
        # os.path.join est plus sûr que de taper des "/" à la main
        image_path = os.path.join('assets', 'images', 'player', 'player.png')
        
        try:
            # 2. On charge l'image
            # convert_alpha() est important pour la transparence (le fond de ton alien)
            self.image = pygame.image.load(image_path).convert_alpha()
            
            # 3. (Optionnel) Si l'image est trop grande ou trop petite, on la redimensionne
            # On la force à faire la taille définie dans settings (ex: 30x30)
            self.image = pygame.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))
            
        except FileNotFoundError:
            # C'est une sécurité : si le fichier n'est pas trouvé, on crée le carré bleu par défaut
            print(f"ERREUR: Image non trouvée à {image_path}. Utilisation du carré bleu.")
            self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
            self.image.fill(COLOR_PLAYER)

        # Le reste ne change pas : on récupère le rectangle de l'image pour gérer la position
        self.rect = self.image.get_rect(topleft=PLAYER_START_POS)
        self.start_pos = PLAYER_START_POS

    def move(self):
        # La logique de mouvement reste exactement la même
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
        # On dessine l'image au lieu du carré
        screen.blit(self.image, self.rect)

    def reset(self):
        self.rect.topleft = self.start_pos