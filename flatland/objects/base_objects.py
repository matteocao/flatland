import copy
import math
import random
from abc import ABC, abstractmethod
from typing import Any, Optional

import pygame

from ..actions.volition import VolitionEngine
from ..consts import TILE_SIZE, Direction
from ..interactions.command import InteractionCommand
from ..interactions.interactions import ContactInteractionMixin
from ..interactions.scheduler import InteractionScheduler
from ..internal.state import InternalState
from ..logger import Logger


# ---------- composite pattern ------------
class GameObject:
    def __init__(self, x: int, y: int, name: str, health: float):
        """
        x, y are the positions
        """
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.name = name
        self.health = health
        self.scheduler = InteractionScheduler(interval=1.0)
        self.logger = Logger()
        self.volition = VolitionEngine(owner=self)
        self.direction: Direction = Direction.DOWN
        self.inertia: int = 0  # shall be >= 0. This is the current speed
        self.acceleration: int = 0  # shall be >= 0.
        self.temperature: float = 36.5
        self.charge: float = 0
        self.actions_per_second: int = 1
        self.last_action_time: float = 0.0
        self.wetness: float = 0.0
        self.mass: float = 2.2
        self.height: float = 1.0
        self.friction_coefficient: int = 1
        self.animation_index = 0
        self.standing_animation_timer = 0
        self.standing_animation_index = 0
        self.push_animation_timer = 0
        self.push_animation_index = 0
        self.animation_timer = 0
        self.movement_sprites_locations: dict[Direction, list[str]] = {
            Direction.UP: [],
            Direction.DOWN: [],
            Direction.LEFT: [],
            Direction.RIGHT: [],
        }
        self.is_update_just_done: bool = (
            False  # this turns to true when self.update() is called and is set to false when self.prepare is called
        )
        self.new_render_time = 0
        self.last_render_time = 0
        self.parent: Optional["GameObject"] = None
        self.children: list[Optional["GameObject"]] = [None]
        # this is the value that decides the rendering order: the higher, the later it will be rendered.
        self.z_level: float = 0
        self.sprite_size_x: int = 64
        self.sprite_size_y: int = 64
        self.is_grabbable: bool = False

    def update(self, event: Any):
        now = pygame.time.get_ticks()

        if (now - self.last_action_time) / 1000 >= 1 / (self.actions_per_second + 0.0001):
            self.is_update_just_done = True
            self.prev_x = self.x
            self.prev_y = self.y
            self.last_action_time = now
            self.logger.info(f"Update for {self.__class__.__name__}")
            self.scheduler.update()  # x, y may be changed here

    def prepare(self, near_objs: Any) -> bool:
        if self.is_update_just_done:
            self.is_update_just_done = False
            self.logger.info(f"Preparation for {self.__class__.__name__}")
            # prepare interactions
            for near_obj in near_objs:
                self.scheduler.add(InteractionCommand(self, near_obj))
            return True
        return False

    def distance(self, other: Any) -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def clone(self) -> Any:
        return copy.deepcopy(self)


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
        self.internal_state = InternalState(self)
        self.speech = ""

    def update(self, event: Any):
        super().update(event)  # self.is_update_just_done is set to true in here
        if self.is_update_just_done:
            self.volition.update()

    def prepare(self, near_objs: Any):
        check = super().prepare(near_objs)
        if check:
            self.volition.prepare()
            self.internal_state.update(near_objs)


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
        self.color = (0, 0, 255)
