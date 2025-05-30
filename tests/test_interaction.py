import os
import warnings

import pygame

os.environ["SDL_VIDEODRIVER"] = "dummy"  # headless video
pygame.init()
pygame.display.set_mode((1, 1))
try:
    pygame.mixer.init()
except pygame.error as e:
    # fallback: disable sound if mixer init fails (e.g., in CI)
    warnings.warn(f"Could not load mixer, {e}")
    pygame.mixer = None  # type: ignore

from flatland.consts import MAX_X, MAX_Y
from flatland.objects.items import Stone, Sword


def test_interaction() -> None:
    stone = Stone(1, 1, "stone1", 10)
    sword = Sword(1, 2, "sword1", 9)
    health_stone = stone.health
    health_sword = sword.health

    stone.on_contact(sword)
    sword.on_contact(stone)

    assert stone.health < health_stone
    assert sword.health < health_sword
