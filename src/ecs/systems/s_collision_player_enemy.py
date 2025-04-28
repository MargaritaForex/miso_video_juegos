import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.create.prefab_creator import create_explosion
from src.engine.service_locator import ServiceLocator


def system_collision_player_enemy(world: esper.World, player_entity: int, level_cfg: dict, explosion_info: dict):
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    pl_rect = CSurface.get_area_relative(pl_s.area, pl_t.pos)

    components = world.get_components(CSurface, CTransform, CTagEnemy)
    for enemy_entity, (c_s, c_t, _) in components:
        ene_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if ene_rect.colliderect(pl_rect):
            # Crear explosión en la posición del enemigo
            explosion_pos = c_t.pos.copy()  # O usa pygame.Vector2(c_t.pos.x, c_t.pos.y)
            create_explosion(world, explosion_pos, explosion_info)
            ServiceLocator.sounds_service.play("assets/snd/explosion.ogg")
            world.delete_entity(enemy_entity)
            # Respawnear jugador en su posición inicial
            spawn_x = level_cfg["player_spawn"]["position"]["x"] - pl_s.surf.get_width() / 2
            spawn_y = level_cfg["player_spawn"]["position"]["y"] - pl_s.surf.get_height() / 2
            pl_t.pos.x = spawn_x
            pl_t.pos.y = spawn_y
            break  # Solo una colisión por frame
