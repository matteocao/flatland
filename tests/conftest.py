import os

os.environ["SDL_VIDEODRIVER"] = "dummy"  # headless video

import pygame
import pytest

from flatland.consts import MAX_X, MAX_Y, TILE_SIZE


@pytest.fixture(scope="session", autouse=True)
def display() -> None:
    pygame.init()
    pygame.display.set_mode((MAX_X * TILE_SIZE, MAX_Y * TILE_SIZE))
