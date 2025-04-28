class CHunterBehavior:
    def __init__(self, origin_pos, chase_distance, return_distance, chase_speed):
        self.origin_pos = origin_pos  # pygame.Vector2
        self.chase_distance = chase_distance
        self.return_distance = return_distance
        self.chase_speed = chase_speed
        self.state = "IDLE"  # Puede ser 'IDLE', 'CHASE', 'RETURN' 