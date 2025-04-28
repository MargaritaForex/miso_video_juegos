import esper
import pygame
import math
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_special_ability import CSpecialAbility
from src.ecs.components.c_text import CText  # 👈 Importamos CText
from src.create.prefab_creator import create_bullet

# Global para almacenar ID del texto (¡no crear mil textos nuevos!)
cooldown_text_entity = None

def system_special_ability(world: esper.World, delta_time: float, bullet_config, event=None):
    global cooldown_text_entity

    components = world.get_components(CPlayerState, CTransform, CSurface, CInputCommand, CSpecialAbility)

    for _, (player, transform, surface, input_command, special_ability) in components:
        # Actualizar cooldown
        if not special_ability.ready:
            special_ability.current_cooldown -= delta_time
            if special_ability.current_cooldown <= 0:
                special_ability.ready = True
                special_ability.current_cooldown = 0

        # ACTUALIZAR el texto de cooldown
        if cooldown_text_entity is None:
            # Crear el texto si no existe aún
            cooldown_text_entity = world.create_entity()
            world.add_component(cooldown_text_entity, CText(
                text="",  # El texto se actualizará abajo
                position=pygame.Vector2(50, 550),  # 📍 Ajusta según tu pantalla
                font_size=16,
                color=pygame.Color('white'),
                centered=False
            ))

        text_component = world.component_for_entity(cooldown_text_entity, CText)
        seconds_left = int(special_ability.current_cooldown)
        text_component.text = f"Recarga especial: {seconds_left}s"
        text_component.dirty = True  # 🧹 ¡Para que se vuelva a dibujar!

        # Activar habilidad especial solo si ready y se presiona E
        if event is not None and event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            if special_ability.ready:
                print("¡Habilidad especial activada!")
                # Crear 8 balas en círculo
                for angle in range(0, 360, 45):
                    angle_rad = math.radians(angle)
                    direction = pygame.Vector2(math.cos(angle_rad), math.sin(angle_rad))
                    create_bullet(
                        world,
                        direction,
                        transform.pos,
                        surface.surf.get_size(),
                        bullet_config
                    )
                special_ability.ready = False
                special_ability.current_cooldown = special_ability.cooldown_time
            else:
                print("Habilidad especial en cooldown")

