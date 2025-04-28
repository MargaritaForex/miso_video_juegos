import esper
import pygame
from src.ecs.components.c_text import CText
from src.engine.service_locator import ServiceLocator


def system_text_rendering(world: esper.World, screen: pygame.Surface):
    components = world.get_component(CText)

    for _, text_comp in components:
        if text_comp.dirty or text_comp.surface is None:
            font = ServiceLocator.fonts_service.get(text_comp.font, text_comp.font_size)
            text_comp.surface = font.render(text_comp.text, True, text_comp.color)
            text_comp.dirty = False

        position = pygame.Vector2(text_comp.position)
        if text_comp.centered:
            position.x -= text_comp.surface.get_width() // 2
            position.y -= text_comp.surface.get_height() // 2

        if text_comp.hidden:
            text_comp.surface.set_alpha(0)
        else:
            screen.blit(text_comp.surface, position)
