import pygame


class SoundsService:
    def __init__(self) -> None:
        self.sounds = {}

    def play(self, sound_name: str) -> None:
        if sound_name not in self.sounds:
            self.sounds[sound_name] = pygame.mixer.Sound(sound_name)
        self.sounds[sound_name].play()
