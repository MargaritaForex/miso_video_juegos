class CSpecialAbility:
    def __init__(self, cooldown_time: float = 5.0):
        self.cooldown_time = cooldown_time
        self.current_cooldown = cooldown_time
        self.ready = False
