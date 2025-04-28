import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.create.prefab_creator import create_explosion
from src.engine.service_locator import ServiceLocator


def system_collision_enemy_bullet(world: esper.World, explosion_info: dict):
    components_enemy = world.get_components(CSurface, CTransform, CTagEnemy)
    components_bullet = world.get_components(CSurface, CTransform, CTagBullet)

    for enemy_entity, (c_s, c_t, _) in components_enemy:
        ene_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        for bullet_entity, (c_b_s, c_b_t, _) in components_bullet:
            bull_rect = c_b_s.area.copy()
            bull_rect.topleft = c_b_t.pos
            if ene_rect.colliderect(bull_rect):
                # Crear explosión en la posición del enemigo
                explosion_pos = c_t.pos.copy()
                create_explosion(world, explosion_pos, explosion_info)
                ServiceLocator.sounds_service.play("assets/snd/explosion.ogg")
                ServiceLocator.sounds_service.play("assets/snd/laser_special.ogg")
                ServiceLocator.sounds_service.play("assets/snd/ufo.ogg")
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)
                break  # Solo una colisión por bala
