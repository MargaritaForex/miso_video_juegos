class CSpecialAbility:
    def __init__(self, cooldown_time: float = 5.0):
        self.cooldown_time = cooldown_time
        self.current_cooldown = 0  # Empieza en 0 para estar listo
        self.ready = True  # Empieza listo para pruebas
