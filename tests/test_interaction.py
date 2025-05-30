import os
import warnings

os.environ["SDL_VIDEODRIVER"] = "dummy"  # headless video

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
