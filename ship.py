import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """Inicializa la nave y fija su posición inicial"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Cargar la imagen de la nave, y obtener su rect
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Comienza cada nave en la parte inferior central de la pantalla
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

         # Almacena un valor decimal para el centro de la nave
        self.center = float(self.rect.centerx)

        # Direcciones de movimiento
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        """Centra la nave en la pantalla"""
        self.center = self.screen_rect.centerx

    def update(self):
        """Actualiza la posición de la nave, basándose en las direcciones de movimiento"""
        # Actualiza el valor del centro de la nave, no el rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

         # Actualiza el objeto rect desde self.center
        self.rect.centerx = self.center

    def blitme(self):
        """Dibuja el barco en su ubicación actual"""
        self.screen.blit(self.image, self.rect)