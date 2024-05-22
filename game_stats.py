class GameStats:
    """Sigue las estadísticas de Alien Invasion"""

    def __init__(self, ai_settings):
        """Inicializar estadísticas"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Iniciar el juego en estado inactivo.
        self.game_active = False

        # El puntaje alto nunca debe ser reiniciado
        self.high_score = 0

    def reset_stats(self):
        """Inicializar las estadísticas que pueden cambiar durante el juego."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1