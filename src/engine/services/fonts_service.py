import pygame


class FontsService:
    def __init__(self) -> None:
        self.fonts = {}
        self.fonts_path = 'assets/fnt/'

    def get(self, font: str, size: int) -> pygame.font.Font:
        key = f"{font}_{size}"
        if key not in self.fonts:
            self.fonts[key] = pygame.font.Font(self.fonts_path + font, size)
        return self.fonts[key]
