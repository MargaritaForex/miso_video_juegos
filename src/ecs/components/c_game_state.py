from enum import Enum

class GameState(Enum):
    RUNNING = 0
    PAUSED = 1

class CGameState:
    def __init__(self) -> None:
        self.state = GameState.RUNNING
        self.pause_text_entity = None
