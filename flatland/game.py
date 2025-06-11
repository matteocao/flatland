import warnings
from typing import Any

import pygame

from .consts import MAX_X, MAX_Y, TILE_SIZE
from .logger import Logger
from .objects import items
from .world.level import Level
from .world.world import world

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

    def __init__(self) -> None:
        if not hasattr(self, "current_level"):  # these checks are needed for the singleton
            self.current_level: Level = Level()
        if not hasattr(self, "world"):
            self.world = world
        if not hasattr(self, "screen"):
            self.screen = pygame.display.set_mode((MAX_X * TILE_SIZE, MAX_Y * TILE_SIZE))
        if not hasattr(self, "clock"):
            self.clock = pygame.time.Clock()
        if not hasattr(self, "logger"):
            self.logger = Logger()

    def main(self) -> None:

        pygame.display.set_caption("Flatland")

        self.current_level = self.world["level_0"]
        self.current_level.get_ground_objs(self)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill((0, 0, 0))  # to cancel previous state
            self.current_level.reset_is_walkable()  # reset tiles to walkable: they will be changed when they are encumbered by objects

            keys = pygame.key.get_pressed()

            # send keys to the user
            if any(keys):
                self.current_level.send_keys_to_user(keys)
            near_objs = self.current_level._observers
            # self.logger.info(near_objs)
            self.current_level.prepare(near_objs, self)
            self.current_level.update(keys)
            self.current_level.correct_periodic_positions()  # this is needed now that the self.current_level is periodic
            self.current_level.render(self.screen)
            pygame.display.flip()
            self.clock.tick(10)

        pygame.quit()
