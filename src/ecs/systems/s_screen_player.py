import pygame
import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator


def system_screen_player(world: esper.World, screen: pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CVelocity, CTagPlayer)
    for _, (c_t, c_s, c_v, c_tag) in components:
        dir_y = 0
        dir_x = 0
        if c_tag.up:
            dir_y -= 1
        if c_tag.down:
            dir_y += 1
        if c_tag.left:
            dir_x -= 1
        if c_tag.right:
            dir_x += 1

        # Sonido de movimiento solo si hay movimiento
        if dir_x != 0 or dir_y != 0:
            ServiceLocator.sounds_service.play("assets/snd/ufo.ogg")

        c_v.vel.x = dir_x * c_tag.velocity
        c_v.vel.y = dir_y * c_tag.velocity

        player_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if not screen_rect.contains(player_rect):
            player_rect.clamp_ip(screen_rect)
            c_t.pos.xy = player_rect.topleft
