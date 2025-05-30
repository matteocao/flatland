import os
from typing import Any

import pygame

os.environ["SDL_VIDEODRIVER"] = "dummy"  # Use a headless display
pygame.init()
pygame.display.set_mode((1, 1))  # Minimal dummy window
import pytest

from flatland.llm_stub import LLMNPCBrain
from flatland.objects.items import Cow, Player, Stone
from flatland.world.world import World


@pytest.fixture
def dummy_screen() -> Any:
    pygame.init()
    return pygame.display.set_mode((320, 320))


def test_player_creation() -> None:
    p = Player(x=1, y=2, name="John", health=10)
    assert p.x == 1 and p.y == 2


def test_stone_push() -> None:
    world = World()
    player = Player(1, 1, "Mark", 2)
    stone = Stone(2, 1, "a rock", 15)


def test_animal_vision_chase() -> None:
    animal = Cow(1, 1, "lola", 2, 2, 3)
    player = Player(x=3, y=1, name="Matt", health=2)


def test_npc_brain():

    brain = LLMNPCBrain("Bob", "friendly")
    for event in [
        "met player",
        "saw stone",
        "heard noise",
        "saw animal",
        "walked north",
        "talked to player",
    ]:
        brain.observe(event)
    assert brain.decide_action() == "reflect"
    assert "Bob" in brain.speak()
