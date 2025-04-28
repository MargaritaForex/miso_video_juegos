import esper
import pygame
from src.ecs.components.c_game_state import CGameState
from src.ecs.components.c_text import CText
from src.create.prefab_creator import create_text


def system_game_state(world: esper.World, event: pygame.event.Event):
    # Obtener el componente de estado del juego
    game_state = world.get_component(CGameState)
    if not game_state:
        return

    _, c_game_state = game_state[0]  # Tomamos el primer (y único) componente de estado

    # Manejar evento de pausa
    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
        c_game_state.is_paused = not c_game_state.is_paused

        # Si no existe el texto de pausa, lo creamos
        if c_game_state.pause_text_entity is None:
            c_game_state.pause_text_entity = create_text(
                world=world,
                text="PAUSED",
                position=pygame.Vector2(400, 300),  # Posición central de la pantalla
                font_size=40,
                color=pygame.Color(255, 255, 255),
                centered=True,
                hidden=True
            )

        # Obtener el componente de texto
        text_comp = world.component_for_entity(c_game_state.pause_text_entity, CText)
        text_comp.hidden = not c_game_state.is_paused  # Mostrar/ocultar según el estado de pausa
