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

    components = world.get_components(CPlayerState, CTransform, CSurface, CSpecialAbility)
    print(f"[DEBUG] Jugadores con habilidad especial: {len(components)}")

    # Buscar el texto de porcentaje especial
    percent_text_entity = None
    for ent, c_text in world.get_component(CText):
        if c_text.text.endswith("%"):
            percent_text_entity = ent
            break

    for _, (player, transform, surface, special_ability) in components:
        print(f"[DEBUG] Cooldown actual: {special_ability.current_cooldown}, Ready: {special_ability.ready}")
        # Actualizar cooldown
        if not special_ability.ready:
            special_ability.current_cooldown -= delta_time
            print(f"[DEBUG] Bajando cooldown: {special_ability.current_cooldown}")
            if special_ability.current_cooldown <= 0:
                special_ability.ready = True
                special_ability.current_cooldown = 0
                print("[DEBUG] Habilidad especial lista para usarse!")

        # Actualizar el texto de porcentaje especial
        if percent_text_entity is not None:
            percent_text = world.component_for_entity(percent_text_entity, CText)
            percent = 100 - int((special_ability.current_cooldown / special_ability.cooldown_time) * 100) if special_ability.cooldown_time > 0 else 100
            if special_ability.ready:
                percent = 100
            percent_text.text = f"{percent}%"
            percent_text.dirty = True

        # ACTUALIZAR el texto de cooldown (opcional, puedes dejarlo si quieres ver segundos)
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
            print("[DEBUG] Evento KEYDOWN de E detectado")
            if special_ability.ready:
                print("¡Habilidad especial activada!")
                # Crear balas en círculo (12 balas, cada 30 grados)
                player_center = pygame.Vector2(
                    transform.pos.x + (surface.surf.get_width() / 2),
                    transform.pos.y + (surface.surf.get_height() / 2)
                )
                for angle in range(0, 360, 30):
                    angle_rad = math.radians(angle)
                    target_x = player_center.x + 100 * math.cos(angle_rad)
                    target_y = player_center.y + 100 * math.sin(angle_rad)
                    target_pos = pygame.Vector2(target_x, target_y)
                    create_bullet(
                        world,
                        target_pos,
                        player_center,
                        surface.surf.get_size(),
                        bullet_config
                    )
                special_ability.ready = False
                special_ability.current_cooldown = special_ability.cooldown_time
            else:
                print("[DEBUG] Habilidad especial en cooldown")

