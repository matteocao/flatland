import copy
import math
import random
from abc import ABC, abstractmethod
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
        self.inertia: float = 0.0  # shall be >= 0. This is the current speed
        self.acceleration: int = 0  # shall be >= 0.
        self.temperature: float = 36.5
        self.charge: float = 0
        self.actions_per_second: int = 1
        self.wetness: float = 0.0
        self.mass: float = 2.2
        self.height: float = 1.0
        self.friction_coefficient: float = 1.0
        self.animation_index = 0
        self.last_tick: int = 0
        self.standing_animation_timer = 0
        self.standing_animation_index = 0
        self.push_animation_timer = 0
        self.push_animation_index = 0
        self.dying_animation_timer = 0
        self.dying_animation_index = 0
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

    def update(self, event: Any):
        now = pygame.time.get_ticks()  # in ms
        interval = 1000 / self.actions_per_second
        tick = int(now // interval)

        if tick != self.last_tick:
            self.last_tick = tick
            self.is_update_just_done = True
            self.prev_x = self.x
            self.prev_y = self.y
            self.logger.info(f"Update for {self.__class__.__name__}")
            self.scheduler.update()  # x, y may be changed here

    def prepare(self, near_objs: Any, game: "Game") -> bool:
        if self.is_update_just_done:
            self.is_update_just_done = False
            self.logger.info(f"Preparation for {self.__class__.__name__}")
            # prepare interactions
            for near_obj in near_objs:
                self.scheduler.add(InteractionCommand(self, near_obj, game))
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

    def prepare(self, near_objs: Any, game: "Game"):
        check = super().prepare(near_objs, game)
        if check:
            self.volition.prepare(game)
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
