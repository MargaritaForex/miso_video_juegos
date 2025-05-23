from enum import Enum
import pygame


class CInputCommand:
    def __init__(self, name: str, keys: [int]) -> None:
        self.name = name
        self.keys = keys
        self.phase = CommandPhase.NA
        self.mouse_pos = pygame.Vector2(0, 0)


class CommandPhase(Enum):
    NA = 0
    START = 1
    END = 2
