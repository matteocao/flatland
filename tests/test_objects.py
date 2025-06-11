import os
from typing import Any

import pygame
import pytest

from flatland.consts import MAX_X, MAX_Y, TILE_SIZE
from flatland.llm_stub import LLMNPCBrain
from flatland.objects.items import Cow, Player, Stone
from flatland.world.world import world


def test_player_creation() -> None:
    p = Player(x=1, y=2, name="John", health=10, vision_range=3, hearing_range=3)
    assert p.x == 1 and p.y == 2


def test_stone_push() -> None:
    player = Player(1, 1, "Mark", 2, vision_range=3, hearing_range=3)
    stone = Stone(2, 1, "a rock", 15)


def test_animal_vision_chase() -> None:
    animal = Cow(1, 1, "lola", 2, 2, 3)
    player = Player(x=3, y=1, name="Matt", health=2, vision_range=3, hearing_range=3)


def test_cow() -> None:
    cow = Cow(1, 1, "lola", 4, 3, 3)
    assert "speak" in dir(cow)
    assert hasattr(cow, "speak")
    assert callable(getattr(cow, "speak", None))


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
