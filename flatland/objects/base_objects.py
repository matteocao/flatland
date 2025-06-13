import copy
import math
import random
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional

import pygame

from ..actions.volition import VolitionEngine
from ..consts import TILE_SIZE, Direction
from ..interactions.command import InteractionCommand
from ..interactions.interactions import ContactInteractionMixin
from ..interactions.scheduler import InteractionScheduler
from ..internal.state import InternalState
from ..logger import Logger

if TYPE_CHECKING:
    from ..__main__ import Game


# ---------- composite pattern ------------
class GameObject:
    def __init__(self, x: int, y: int, name: str, health: float):
        """
        x, y are the positions
        """
        self.id = uuid.uuid4().hex
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.name = name
        self.health = health
        self.scheduler = InteractionScheduler(interval=1.0)
        self.logger = Logger()
        self.volition = VolitionEngine(owner=self)
        self.internal_state = InternalState(self)
        self.vision_range = 0
        self.hearing_range = 0
        self.direction: Direction = Direction.DOWN
        self.inertia: float = 0.0  # shall be >= 0. This is the current speed
        self.acceleration: int = 0  # shall be >= 0.
        self.temperature: float = 36.5
        self.charge: float = 0
        self.actions_per_second: int = 1
        self.render_on_top_of_parent: bool = False
        self.wetness: float = 0.0
        self.mass: float = 2.2
        self.location_as_parent: bool = False
        self.height: float = 1.0
        self.friction_coefficient: float = 1.0
        self.is_moving = False
        self.last_tick: int = 0
        self.is_standing = True
        self.is_pushing = False
        self.is_prepare_just_done: bool = (
            False  # this turns to true when self.update() is called and is set to false when self.prepare is called
        )
        self._parent: Optional["GameObject"] = None
        self.parent_id: Optional[str] = None
        self.children: list["GameObject"] = []
        # this is the value that decides the rendering order: the higher, the later it will be rendered.
        self.z_level: float = 0
        self.sprite_size_x: int = 64
        self.sprite_size_y: int = 64
        self.is_grabbable: bool = False
        self.inertia_threshold_to_hurt_upper: float = 10.0
        self.inertia_threshold_to_hurt_lower: float = -1.0
        self.temperature_threshold_to_hurt_upper: float = 100.0
        self.temperature_threshold_to_hurt_lower: float = -100.0
        self.equilibrium_temperature: float = 30
        self.is_encumbrant: bool = False
        self.ignore_walkable: bool = False

    def __post_init__(self) -> None:
        if hasattr(self, "create_movement_sprites"):
            self.create_movement_sprites()
        if hasattr(self, "create_dying_sprites"):
            self.create_dying_sprites()
        if hasattr(self, "create_standing_sprites"):
            self.create_standing_sprites()
        if hasattr(self, "create_push_sprites"):
            self.create_push_sprites()

    @property
    def parent(self) -> Optional["GameObject"]:
        return self._parent

    @parent.setter
    def parent(self, value: Optional["GameObject"]) -> None:
        self._parent = value
        if value is not None:
            self.parent_id = value.id

    def update(self, event: Any) -> bool:
        if self.is_prepare_just_done:
            self.is_prepare_just_done = False
            self.logger.info(f"Update for {self.__class__.__name__}")
            self.volition.update()
            self.scheduler.update()  # this runs all teh interaction callables
            # animation flags:
            if self.prev_x != self.x or self.prev_y != self.y:
                self.is_pushing = False
                self.is_moving = True
                self.is_standing = False
            elif (
                self.prev_x == self.x
                and self.prev_y == self.y
                and any("push" == func.__name__ for func, _ in self.volition.list_of_actions)
            ):
                self.is_pushing = True
                self.is_moving = False
                self.is_standing = False
            elif self.prev_x == self.x and self.prev_y == self.y:
                self.is_pushing = False
                self.is_moving = False
                self.is_standing = True
            return True
        return False

    def prepare(self, near_objs: Any, game: "Game") -> bool:
        now = pygame.time.get_ticks()  # in ms
        interval = 1000 / self.actions_per_second
        tick = int(now // interval)

        if tick != self.last_tick:
            self.prev_x = self.x
            self.prev_y = self.y
            self.last_tick = tick
            self.logger.info(f"Preparation for {self.__class__.__name__}")
            # prepare interactions
            for near_obj in near_objs:
                self.scheduler.add(InteractionCommand(self, near_obj, game))
            self.volition.prepare(game)
            self.internal_state.update(near_objs)
            self.is_prepare_just_done = True
            return True
        return False

    def distance(self, other: Any) -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class BaseAnimal(GameObject):
    def __init__(
        self,
        x: int,
        y: int,
        name: str,
        health: float,
        vision_range: int,
        hearing_range: int,
    ):
        super().__init__(x, y, name, health)
        self.vision_range = vision_range
        self.hearing_range = hearing_range
        self.speech = ""


class BaseNPC(BaseAnimal):
    def __init__(
        self,
        x: int,
        y: int,
        name: str,
        health: float,
        vision_range: int,
        hearing_range: int,
    ):
        super().__init__(x, y, name, health, vision_range, hearing_range)
