import os
import warnings
from typing import Any

import pygame
import pytest

from flatland.objects.items import Stone


def test_interaction(display) -> None:
    stone = Stone(1, 1, "stone1", 10)
    stone2 = Stone(1, 1, "stone2", 9)
    stone2.inertia = 4.0
    stone.inertia = 2.0
    health_stone = stone.health
    health_stone2 = stone2.health

    stone.on_contact(stone2)
    stone2.on_contact(stone)
    assert stone.health == health_stone
    assert stone2.health == health_stone2

    stone.damage_by_inertia()
    stone2.damage_by_inertia()

    assert stone.health < health_stone
    assert stone2.health < health_stone2
