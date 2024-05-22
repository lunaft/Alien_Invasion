import pygame.font


class Button:
    def __init__(self, ai_settings, screen, msg):
        """Inicializar los botones"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Establece las dimensiones y propiedades del botón
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Construye el objeto rect del botón y lo centra
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # El mensaje del botón sólo lo muestra una vez
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Convierte el msg en una imagen renderizada y centra el texto en el botón"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Dibujar botón en blanco, luego dibujar mensaje
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)