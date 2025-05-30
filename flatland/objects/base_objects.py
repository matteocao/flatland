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


class GameObject(ABC):
    def __init__(self, x: int, y: int, name: str, health: int):
        """
        x, y are the positions
        """
        self.x = x
        self.y = y
        self.name = name
        self.health = health
        self.scheduler = InteractionScheduler(interval=1.0)
        self.volition = VolitionEngine(owner=self)
        self.logger = Logger()
        self.direction: Direction = Direction.DOWN
        self.speed: int = 0  # shall be >= 0. This is the current speed
        self.actions_per_second: int = 1
        self.last_action_time: float = 0.0

    def update(self, event: Any):
        now = pygame.time.get_ticks()
        if now - self.last_action_time >= 1 / self.actions_per_second:
            self.last_action_time = now
            self.logger.info(f"Update for {self.__class__.__name__}")
            self.scheduler.update()

    def prepare(self, near_objs: Any):
        self.logger.info(f"Preparation for {self.__class__.__name__}")
        # prepare interactions
        for near_obj in near_objs:
            self.scheduler.add(InteractionCommand(self, near_obj))

    def distance(self, other: Any) -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    @abstractmethod
    def render(self, screen: pygame.Surface):
        pass


class BaseAnimal(GameObject):
    def __init__(
        self,
        x: int,
        y: int,
        name: str,
        health: int,
        vision_range: int,
        hearing_range: int,
    ):
        super().__init__(x, y, name, health)
        self.color = (255, 255, 0)
        self.vision_range = vision_range
        self.hearing_range = hearing_range
        self.internal_state = InternalState(self)

    def update(self, event: Any):
        super().update(event)
        now = pygame.time.get_ticks()
        if now - self.last_action_time >= 1 / self.actions_per_second:
            self.volition.update()

    def prepare(self, near_objs: Any):
        super().prepare(near_objs)
        self.volition.prepare()
        self.internal_state.update(near_objs)

    def render(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )


class BaseNPC(BaseAnimal):
    def __init__(
        self,
        x: int,
        y: int,
        name: str,
        health: int,
        vision_range: int,
        hearing_range: int,
    ):
        super().__init__(x, y, name, health, vision_range, hearing_range)
        self.color = (0, 0, 255)

    def render(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )
