class Settings:
    """Una clase para almacenar todos los ajustes de Alien Invasion"""

    def __init__(self):
        """Inicializar los ajustes estáticos del juego"""
        # Ajustes de pantalla
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Configuración de la nave
        self.ship_limit = 3

        # Configuración de la bala.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # Configuración de Alien.
        self.fleet_drop_speed = 10

        # Cómo de rápido se acelera el juego.
        self.speedup_scale = 1.1
        # Cómo de rápido aumentan los valores de puntos de los alienígenas.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inicializa los ajustes que cambian a lo largo del juego"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.3

        # Puntuación
        self.alien_points = 50

        # fleet_direction de 1 representa derecha, -1 representa izquierda
        self.fleet_direction = 1

    def increase_speed(self):
        """Incrementa la configuración de velocidad y los valores de puntos alienígenas"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)