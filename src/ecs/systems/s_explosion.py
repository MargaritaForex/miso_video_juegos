import esper
from src.ecs.components.c_explosion import CExplosion


def system_explosion(world: esper.World, delta_time: float):
    entities_to_remove = []
    for entity, (explosion_component,) in world.get_components(CExplosion):
        explosion_component.time_remaining -= delta_time
        if explosion_component.time_remaining <= 0:
            entities_to_remove.append(entity)
    for entity in entities_to_remove:
        world.delete_entity(entity, True)
