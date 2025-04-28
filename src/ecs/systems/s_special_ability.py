import esper
import pygame
import math
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_special_ability import CSpecialAbility
from src.create.prefab_creator import create_bullet


# from src.engine.service_locator import ServiceLocator  # Descomenta si tienes sonido

def system_special_ability(world: esper.World, delta_time: float, bullet_config):
    components = world.get_components(CPlayerState, CTransform, CSurface, CInputCommand, CSpecialAbility)

    for _, (player, transform, surface, input_command, special_ability) in components:
        # Cooldown
        if not special_ability.ready:
            special_ability.current_cooldown -= delta_time
            if special_ability.current_cooldown <= 0:
                special_ability.ready = True
                special_ability.current_cooldown = 0

        # Input especial (tecla E)
        keys = pygame.key.get_pressed()

        # 🛠️ Prints de debug para ver qué pasa
        print("Special ready:", special_ability.ready)
        print("Cooldown actual:", special_ability.current_cooldown)
        print("Tecla E presionada:", keys[pygame.K_e])

        if special_ability.ready and keys[pygame.K_e]:
            player_center = pygame.Vector2(
                transform.pos.x + (surface.area.width / 2),
                transform.pos.y + (surface.area.height / 2)
            )

            # Crear disparos en círculo
            for angle in range(15, 375, 30):
                radians = math.radians(angle)
                target_x = player_center.x + 100 * math.cos(radians)
                target_y = player_center.y + 100 * math.sin(radians)
                target_pos = pygame.Vector2(target_x, target_y)
                create_bullet(world, target_pos, player_center, surface.area.size, bullet_config)

            # Si tienes sonido, puedes descomentar esta línea:
            # ServiceLocator.sounds_service.play("assets/snd/laser_special.ogg")

            special_ability.ready = False
            special_ability.current_cooldown = special_ability.cooldown_time
