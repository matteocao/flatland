"""
world
"""

from typing import TYPE_CHECKING, Any

import pygame

from ..consts import MAX_X, MAX_Y
from ..logger import Logger

if TYPE_CHECKING:
    from ..__main__ import Game
    from ..objects.base_objects import GameObject


# --------------------- implemented via observer pattern ----------------
class Level:
    """
    The level, treated as a subject to which all objects register to.
    Via the observer method, the world loops through the objects and updates them.
    """

    def __init__(self) -> None:
        self._observers: list["GameObject"] = []
        self._scheduled_to_die: list[tuple["GameObject", int, int]] = []
        self.logger = Logger()

    def register(self, obj: "GameObject") -> None:
        if obj not in self._observers:
            self.logger.info(f"Register to world {obj}")
            self._observers.append(obj)

    def send_keys_to_user(self, keys) -> None:
        for observer in self._observers:
            if hasattr(observer, "get_pressed_keys"):
                observer.get_pressed_keys(keys)

    def get_ground_objs(self, game: "Game"):
        for obj in self._observers:
            if hasattr(obj, "get_ground_objs"):
                obj.get_ground_objs(game)

    def unregister(self, obj: "GameObject") -> None:
        if obj in self._observers:
            self._observers.remove(obj)

    def update(self, event: Any) -> None:
        for observer in self._observers:
            observer.update(event)
        now = pygame.time.get_ticks()
        for obj, dt, t in self._scheduled_to_die:
            if t + dt < now:
                self.unregister(obj)
                self._scheduled_to_die.remove((obj, dt, t))

    def prepare(self, near_objs: Any, game: "Game") -> None:
        for obj in self._observers:
            obj.prepare(near_objs, game)

    def reset_is_walkable(self) -> None:
        for observer in self._observers:
            if hasattr(observer, "reset_is_walkable"):
                observer.reset_is_walkable()

    def correct_periodic_positions(self) -> None:
        for obj in self._observers:
            obj.x = obj.x % MAX_X
            obj.y = obj.y % MAX_Y

    def render(self, screen) -> None:
        for obj in self.order_observers_by_z_level():
            if hasattr(obj, "render"):
                obj.render(screen)

    def order_observers_by_z_level(self) -> list["GameObject"]:
        return sorted(self._observers, key=lambda obj: obj.z_level)

    def schedule_to_unregister(self, obj, timer_ms: int = 1000) -> None:
        now = pygame.time.get_ticks()
        self._scheduled_to_die.append((obj, timer_ms, now))
