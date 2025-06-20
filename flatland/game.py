"""
This file is the main single-player game loop.

This loop is not directly used in the multiplayer game.
"""

import os
import warnings
from typing import Any

import pygame

from .consts import MAX_X, MAX_Y, TILE_SIZE
from .logger import Logger
from .objects.items_registry import registry
from .world.level import Level

os.environ["SDL_VIDEODRIVER"] = "dummy"  # Use a headless display

# initialise pygame for CI tests
pygame.init()
pygame.display.set_mode((1, 1))  # Minimal dummy window
try:
    pygame.mixer.init()
except pygame.error as e:
    # fallback: disable sound if mixer init fails (e.g., in CI)
    warnings.warn(f"Could not load mixer, {e}")


class Game:
    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any):
        if cls._instance is None:
            cls._instance = super(Game, cls).__new__(cls)
        return cls._instance

    def __init__(self, world: dict[str, Level], screen: pygame.Surface) -> None:
        if not hasattr(self, "current_level"):  # these checks are needed for the singleton
            self.current_level: Level = Level()
        if not hasattr(self, "world"):
            self.world = world
        if not hasattr(self, "screen"):
            self.screen = screen
        if not hasattr(self, "clock"):
            self.clock = pygame.time.Clock()
        if not hasattr(self, "logger"):
            self.logger = Logger()

    def get_key_state(self) -> Any:
        return pygame.key.get_pressed()

    def main(self, stop_event: Any = None) -> None:

        pygame.display.set_caption("Flatland")

        self.current_level = self.world["level_0"]
        player = registry.create(
            cls_name="Player",
            x=4,
            y=4,
            name="Matte",
            health=10,
            vision_range=5,
            hearing_range=5,
            temperature=36.3,
        )
        self.current_level.register(player)
        self.current_level.get_ground_objs(self)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.USEREVENT:
                    level_key, exit_name = event.code
                    print(event, level_key)
                    # get player
                    player = [
                        obj
                        for obj in self.current_level._observers
                        if obj.__class__.__name__ == "Player"
                    ][0]
                    # unregister
                    self.current_level.unregister(player)
                    for obj in player.children:
                        self.current_level.unregister(obj)
                    # change level
                    self.current_level = self.world[level_key]
                    portal = [
                        obj for obj in self.current_level._observers if obj.name == exit_name
                    ][0]
                    player.x = portal.x
                    player.y = portal.y
                    self.current_level.register(player)
                    for obj in player.children:
                        obj.x = portal.x
                        obj.y = portal.y
                        self.current_level.register(obj)
                    self.current_level.get_ground_objs(self)
            self.screen.fill((0, 0, 0))  # to cancel previous state
            self.current_level.reset_is_walkable()  # reset tiles to walkable: they will be changed when they are encumbered by objects

            keys = self.get_key_state()  # this does pygame.key.get_pressed()

            # send keys to the user
            if any(keys):
                self.current_level.send_keys_to_user(keys)
            near_objs = self.current_level._observers
            # self.logger.info(near_objs)
            self.current_level.set_volume(player)  # type: ignore
            self.current_level.prepare(near_objs, self)
            self.current_level.update(keys)
            self.current_level.correct_periodic_positions()  # this is needed now that the self.current_level is periodic
            self.current_level.render(self.screen)
            pygame.display.flip()
            self.clock.tick(10)

            if stop_event is not None and stop_event.is_set():
                running = False

        pygame.quit()
