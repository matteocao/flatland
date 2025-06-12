import time

import multiprocess  # type: ignore
import pygame
import pytest

from flatland.consts import Direction
from flatland.game import Game
from flatland.objects.items_registry import registry
from flatland.world.level import Level
from flatland.world.register_to_level import register_terrain


def test_inertia_damage():
    # create a factory to re-create the game inside subprocess
    def game_factory():
        goblin = registry.create(
            cls_name="Goblin",
            x=4,
            y=0,
            name="ashpack",
            health=9,
            vision_range=3,
            hearing_range=5,
        )
        stone = registry.create(
            cls_name="Stone",
            x=0,
            y=0,
            name="a rock",
            health=50,
        )
        stone.direction = Direction.RIGHT
        stone.inertia = 19
        level = Level()
        level.register(stone)
        level.register(goblin)
        level = register_terrain(level, 5, 1)
        world = {"level_0": level}
        display = pygame.display.set_mode((100, 100))
        game = Game(world, display)
        return game

    def run_game(game_factory, stop_event):
        # always initialize pygame inside the child process
        import os

        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()

        game = game_factory()  # re-create the game inside this process
        game.main(stop_event=stop_event)
        goblin = [
            obj for obj in game.current_level._observers if obj.__class__.__name__ == "Goblin"
        ][0]
        assert goblin.health < 9
        stone = [obj for obj in game.current_level._observers if obj.__class__.__name__ == "Stone"][
            0
        ]
        assert stone.health < 50

    # multiprocessing event for shutdown
    multiprocess.set_start_method("spawn", force=True)
    stop_event = multiprocess.Event()

    # spawn the game loop in subprocess
    process = multiprocess.Process(target=run_game, args=(game_factory, stop_event))
    process.start()

    time.sleep(10)

    # trigger external shutdown
    stop_event.set()

    # wait for game to exit
    process.join(timeout=10)

    assert process.exitcode == 0  # ensure clean exit
