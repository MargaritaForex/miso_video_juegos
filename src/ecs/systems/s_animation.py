import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface


def system_animation(world: esper.World, delta_time: CAnimation):
    components = world.get_components(CSurface, CAnimation)

    for _, (c_s, c_a) in components:
        # 1. Disminuir el valor actual del tiempo de la animación
        c_a.curr_anim_time -= delta_time

        # 2. Si el tiempo es menor o igual a 0, se hace cambio de frame
        if c_a.curr_anim_time <= 0:
            # 2.1 Reiniciar el tiempo
            c_a.curr_anim_time = c_a.animations_list[c_a.curr_anim].framerate
            # 3. Cambiar el frame
            c_a.curr_anim_time += 1

            # 4. Limitar el frame actual al rango de la animación
            if c_a.curr_frame > c_a.animations_list[c_a.curr_anim].end:
                c_a.curr_frame = c_a.animations_list[c_a.curr_anim].start
                # Calcular la nueva subtarea del rectangulo de sprite
            rect_surf = c_s.surf.get_rect()
            c_s.area.w = rect_surf.w / c_a.number_frames
            c_s.area.x = c_s.area.w * c_a.curr_frame
