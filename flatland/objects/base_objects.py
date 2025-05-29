import random
from abc import ABC, abstractmethod
from typing import Any

import pygame

from ..consts import TILE_SIZE
from ..interactions.interactions import ContactInteractionMixin


class GameObject(ABC):
    def __init__(self, x: int, y: int, name: str, health: int):
        """
        x, y are the positions
        """
        self.x = x
        self.y = y
        self.name = name
        self.health = health

    @abstractmethod
    def update(self, event: Any):
        pass

    @abstractmethod
    def prepare(self, event: Any):
        pass

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

    def render(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )

    def prepare(self, event: Any):
        pass

    def update(self, event: Any):
        pass


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

    def prepare(self, event: Any):
        pass

    def update(self, event: Any):
        pass
