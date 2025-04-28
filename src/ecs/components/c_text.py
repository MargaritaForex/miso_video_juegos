import pygame


class CText:
    def __init__(self, text: str,
                 position: pygame.Vector2,
                 font_size: int,
                 color: pygame.Color,
                 font: str = 'PressStart2P.ttf',
                 centered: bool = False,
                 hidden: bool = False) -> None:
        self.text = text
        self.position = position
        self.font = font
        self.font_size = font_size
        self.color = color
        self.centered = centered
        self.dirty = True  # Indica si el texto debe ser renderizado de nuevo
        self.surface = None  # Superficie donde se renderiza el texto
        self.hidden = hidden  # Indica si el texto debe estar oculto
