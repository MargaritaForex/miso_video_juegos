import pygame
import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_hunter_behavior import CHunterBehavior
from src.ecs.components.tags.c_tag_hunter import CTagHunter


def system_hunter_behavior(world: esper.World, player_pos: pygame.Vector2):
    components = world.get_components(CTransform, CVelocity, CHunterBehavior, CTagHunter)
    for _, (c_t, c_v, c_h, _) in components:
        dist_to_player = (player_pos - c_t.pos).length()
        dist_to_origin = (c_h.origin_pos - c_t.pos).length()
        if c_h.state == "IDLE":
            if dist_to_player < c_h.chase_distance:
                c_h.state = "CHASE"
        if c_h.state == "CHASE":
            if dist_to_origin > c_h.return_distance:
                c_h.state = "RETURN"
            else:
                direction = (player_pos - c_t.pos).normalize()
                c_v.vel = direction * c_h.chase_speed
        if c_h.state == "RETURN":
            if dist_to_origin < 1.0:
                c_h.state = "IDLE"
                c_v.vel = pygame.Vector2(0, 0)
            else:
                direction = (c_h.origin_pos - c_t.pos).normalize()
                c_v.vel = direction * c_h.chase_speed
