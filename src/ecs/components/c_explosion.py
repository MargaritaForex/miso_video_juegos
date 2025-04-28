class CExplosion:
    def __init__(self, duration: float) -> None:
        self.duration = duration
        self.time_remaining = duration
        self.should_remove = False
