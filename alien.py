import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """AUna clase para representar a un único alienígena de la flota"""

    def __init__(self, ai_settings, screen):
        """Inicializa el alien, y establece su posición inicial"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Carga la imagen del alien, y establece su atributo rect
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Comienza cada nuevo alien cerca de la parte superior izquierda de la pantalla
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Almacena la posición exacta del alien
        self.x = float(self.rect.x)

    def check_edges(self):
        """Devuelve True si el alien está en el borde de la pantalla"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Mueve al alien a la derecha o a la izquierda"""
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def blitme(self):
        """Dibuja al alien en su posición actual"""
        self.screen.blit(self.image, self.rect)