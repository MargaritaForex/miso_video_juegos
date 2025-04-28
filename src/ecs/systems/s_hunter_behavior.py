import pygame
import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_hunter_behavior import CHunterBehavior
from src.ecs.components.tags.c_tag_hunter import CTagHunter
from src.ecs.components.c_animation import CAnimation

def _set_hunter_animation(c_a: CAnimation, anim_name: str):
    if c_a.animations_list[c_a.curr_anim].name == anim_name:
        return
    for idx, anim in enumerate(c_a.animations_list):
        if anim.name == anim_name:
            c_a.curr_anim = idx
            c_a.curr_anim_time = 0
            c_a.curr_frame = anim.start
            break

def system_hunter_behavior(world: esper.World, player_pos: pygame.Vector2):
    components = world.get_components(CTransform, CVelocity, CHunterBehavior, CTagHunter, CAnimation)
    for _, (c_t, c_v, c_h, _, c_a) in components:
        dist_to_player = (player_pos - c_t.pos).length()
        dist_to_origin = (c_h.origin_pos - c_t.pos).length()
        prev_state = c_h.state
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

        # Cambiar animación según el estado
        if c_h.state == "IDLE":
            _set_hunter_animation(c_a, "IDLE")
        else:
            _set_hunter_animation(c_a, "MOVE")

