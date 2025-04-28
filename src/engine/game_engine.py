import json
import pygame
import esper
import asyncio

from src.ecs.components.c_special_ability import CSpecialAbility
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_animation import system_animation

from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_collision_enemy_bullet import system_collision_enemy_bullet

from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_input import system_input
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_screen_player import system_screen_player
from src.ecs.systems.s_screen_bullet import system_screen_bullet

from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer

from src.ecs.components.c_input_command import CInputCommand, CommandPhase

from src.create.prefab_creator import (
    create_enemy_spawner,
    create_input_player,
    create_player_square,
    create_bullet,
    create_text,
)

from src.ecs.systems.s_explosion import system_explosion
from src.ecs.systems.s_hunter_behavior import system_hunter_behavior
from src.ecs.systems.s_special_ability import system_special_ability

from src.ecs.components.c_text import CText
from src.engine.service_locator import ServiceLocator

from src.ecs.systems.s_text_rendering import SystemTextRendering
from src.ecs.systems.s_game_state import system_game_state

from src.ecs.components.c_player_state import CPlayerState


class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()

        pygame.init()
        pygame.display.set_caption(self.window_cfg["title"])
        self.screen = pygame.display.set_mode(
            (self.window_cfg["size"]["w"], self.window_cfg["size"]["h"]), pygame.SCALED
        )

        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_cfg["framerate"]
        self.delta_time = 0
        self.bg_color = pygame.Color(
            self.window_cfg["bg_color"]["r"],
            self.window_cfg["bg_color"]["g"],
            self.window_cfg["bg_color"]["b"],
        )
        self.ecs_world = esper.World()

        self.num_bullets = 0

        self.ecs_world.add_processor(SystemTextRendering(self.screen), priority=1)

    def _load_config_files(self):
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open("assets/cfg/enemies.json", encoding="utf-8") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open("assets/cfg/level_01.json", encoding="utf-8") as level_01_file:
            self.level_01_cfg = json.load(level_01_file)
        with open("assets/cfg/player.json", encoding="utf-8") as player_file:
            self.player_cfg = json.load(player_file)
        with open("assets/cfg/bullet.json", encoding="utf-8") as bullet_file:
            self.bullet_cfg = json.load(bullet_file)
        with open("assets/cfg/explosion.json", encoding="utf-8") as explosion_file:
            self.explosion_cfg = json.load(explosion_file)

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            await asyncio.sleep(0)
        self._clean()

    def _create(self):
        self._player_entity = create_player_square(
            self.ecs_world, self.player_cfg, self.level_01_cfg["player_spawn"]
        )
        self._player_c_v = self.ecs_world.component_for_entity(
            self._player_entity, CVelocity
        )
        self._player_c_t = self.ecs_world.component_for_entity(
            self._player_entity, CTransform
        )
        self._player_c_s = self.ecs_world.component_for_entity(
            self._player_entity, CSurface
        )
        self._player_tag = self.ecs_world.component_for_entity(
            self._player_entity, CTagPlayer
        )

        create_enemy_spawner(self.ecs_world, self.level_01_cfg)
        create_input_player(self.ecs_world)

        # Crear un texto de ejemplo
        create_text(
            world=self.ecs_world,
            text="¡Hola Mundo!",
            position=pygame.Vector2(400, 300),  # Posición en pantalla
            font_size=20,
            color=pygame.Color(255, 255, 255),  # Color blanco
            centered=True,  # Centrado en la posición
            hidden=False  # Visible
        )

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0
        if self.delta_time > 1 / 30:
            self.delta_time = 1 / 30

    def _process_events(self):
        for event in pygame.event.get():
            print(event)  # <-- Depuración: ver todos los eventos
            system_input(self.ecs_world, event, self._do_action)
            system_game_state(self.ecs_world, event)
            system_special_ability(self.ecs_world, self.delta_time, self.bullet_cfg, event)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_enemy_spawner(self.ecs_world, self.enemies_cfg, self.delta_time)
        system_movement(self.ecs_world, self.delta_time)
        system_player_state(self.ecs_world)

        system_screen_bounce(self.ecs_world, self.screen)
        system_screen_player(
            self.ecs_world, self.player_cfg["input_velocity"], self.screen
        )
        system_screen_bullet(self.ecs_world, self.screen)

        system_collision_enemy_bullet(self.ecs_world, self.explosion_cfg)
        system_collision_player_enemy(
            self.ecs_world, self._player_entity, self.level_01_cfg, self.explosion_cfg
        )

        system_animation(self.ecs_world, self.delta_time)
        player_pos = self._player_c_t.pos
        system_hunter_behavior(self.ecs_world, player_pos)
        system_explosion(self.ecs_world, self.delta_time)
        system_special_ability(self.ecs_world, self.delta_time, self.bullet_cfg)
        self.ecs_world._clear_dead_entities()
        self.num_bullets = len(self.ecs_world.get_component(CTagBullet))


    def _draw(self):
        self.screen.fill(self.bg_color)  # 1. Limpia pantalla
        self.ecs_world.process()  # 2. Procesa sistemas ECS (incluyendo texto)
        system_rendering(self.ecs_world, self.screen)  # 3. Dibuja sprites, fondo, etc
        pygame.display.flip()  # 4. Actualiza ventana

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _do_action(self, c_input: CInputCommand):
        if c_input.name == "PLAYER_LEFT":
            self._player_tag.left = c_input.phase == CommandPhase.START
        if c_input.name == "PLAYER_RIGHT":
            self._player_tag.right = c_input.phase == CommandPhase.START
        if c_input.name == "PLAYER_UP":
            self._player_tag.up = c_input.phase == CommandPhase.START
        if c_input.name == "PLAYER_DOWN":
            self._player_tag.down = c_input.phase == CommandPhase.START

        if (
            c_input.name == "PLAYER_FIRE"
            and self.num_bullets < self.level_01_cfg["player_spawn"]["max_bullets"]
            and c_input.phase == CommandPhase.START
        ):
            create_bullet(
                self.ecs_world,
                c_input.mouse_pos,
                self._player_c_t.pos,
                self._player_c_s.surf.get_size(),
                self.bullet_cfg,
            )

def system_text_rendering(world: esper.World, screen: pygame.Surface):
    components = world.get_component(CText)
    
    for _, text_comp in components:
        # Si el texto está sucio o no tiene superficie, renderiza de nuevo
        if text_comp.dirty or text_comp.surface is None:
            font = ServiceLocator.fonts_service.get(text_comp.font, text_comp.font_size)
            text_comp.surface = font.render(text_comp.text, True, text_comp.color)
            text_comp.dirty = False
        
        # Calcula la posición (centrado si es necesario)
        position = pygame.Vector2(text_comp.position)
        if text_comp.centered:
            position.x -= text_comp.surface.get_width() // 2
            position.y -= text_comp.surface.get_height() // 2

        # Si está oculto, no renderiza
        if text_comp.hidden:
            text_comp.surface.set_alpha(0)
        else:
            screen.blit(text_comp.surface, position)

def system_game_state(world: esper.World, event: pygame.event.Event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
        print("¡PRESIONASTE PAUSA!")

def system_special_ability(world: esper.World, delta_time: float, bullet_config, event=None):
    components = world.get_components(CPlayerState, CTransform, CSurface, CInputCommand, CSpecialAbility)
    print("Componentes encontrados:", len(components))
