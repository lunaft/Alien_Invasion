import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Una clase para gestionar las balas disparadas desde la nave"""

    def __init__(self, ai_settings, screen, ship):
        """Crea un objeto bala, en la posición actual de la nave"""
        super(Bullet, self).__init__()
        self.screen = screen

        # Crea el rectángulo de la bala en (0, 0), luego fija la posición correcta.
        self.rect = pygame.Rect(
            0, 0, ai_settings.bullet_width, ai_settings.bullet_height
        )
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Almacena un valor decimal para la posición de la bala.
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Mueve la bala hacia arriba en la pantalla"""
        # Actualiza la posición decimal de la bala
        self.y -= self.speed_factor
        # Actualiza la posición del rectángulo
        self.rect.y = self.y

    def draw_bullet(self):
        """Dibuja la bala en la pantalla"""
        pygame.draw.rect(self.screen, self.color, self.rect)