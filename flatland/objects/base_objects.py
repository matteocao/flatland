import copy
import math
import random
from abc import ABC, abstractmethod
from typing import Any

import pygame

from ..actions.volition import VolitionEngine
from ..consts import TILE_SIZE, Direction
from ..interactions.command import InteractionCommand
from ..interactions.interactions import ContactInteractionMixin
from ..interactions.scheduler import InteractionScheduler
from ..internal.state import InternalState
from ..logger import Logger


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
        self.new_render_time = 0.0
        self.last_render_time = 0.0

    def create_movement_sprites(self) -> None:
        self.movement_sprites = {
            k: list(map(lambda x: pygame.image.load(x).convert_alpha(), lst_str))
            for k, lst_str in self.movement_sprites_locations.items()
        }

    def update(self, event: Any):
        now = pygame.time.get_ticks()

        if (now - self.last_action_time) / 1000 >= 1 / self.actions_per_second:
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

    def update_animation(self):
        if self.inertia > 0:
            self.animation_timer += 1
            if self.animation_timer >= 10:
                self.animation_timer = 0
                self.animation_index = (self.animation_index + 1) % self.num_animations
        else:
            self.animation_index = 0  # standing still

    def render(self, screen: pygame.Surface):
        now = pygame.time.get_ticks()
        if self.is_update_just_done:
            self.new_render_time = now
        self.last_render_time = now
        alpha = (self.last_render_time - self.new_render_time) / 1000 * self.actions_per_second
        pos = (
            (alpha * self.x + (1 - alpha) * self.prev_x) * TILE_SIZE,
            (alpha * self.y + (1 - alpha) * self.prev_y) * TILE_SIZE,
        )
        self.update_animation()
        sprite = self.movement_sprites[self.direction][self.animation_index]
        screen.blit(sprite, pos)


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
        self.color = (255, 255, 0)
        self.volition = VolitionEngine(owner=self)
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
