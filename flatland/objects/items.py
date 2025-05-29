from typing import Any

import pygame

from ..actions.actions import LimbControlMixin, MovementMixin, SpeechMixin
from ..consts import MAX_X, MAX_Y, TILE_SIZE
from ..interactions.interactions import (ContactInteractionMixin,
                                         HeatInteractionMixin)
from ..internal.state import InternalState
from ..sensors.sensors import HearingSensorMixin, SightSensorMixin
from .base_objects import BaseAnimal, BaseNPC, GameObject
from .items_registry import registry


@registry.register
class Stone(ContactInteractionMixin, GameObject):
    def __init__(self, x: int, y: int, name: str, health: int, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.color = (128, 128, 128)
        self.moving = False
        self.noise_intensity = 0.1
        self.attractiveness = 0.1
        self.visible_size = 0.5

    def contact_effect(self, other):
        if isinstance(other, Sword):
            self.health -= 1
            print(f"{self.name} chips! Durability: {self.health}")

    def render(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )


@registry.register
class HeatedStone(ContactInteractionMixin, HeatInteractionMixin, GameObject):
    def __init__(
        self, x: int, y: int, name: str, health: int, temperature: float, **kwargs: Any
    ) -> None:
        super().__init__(x, y, name, health)
        self.temperature = temperature
        self.noise_intensity = 0.1
        self.attractiveness = 0.1
        self.visible_size = 0.5

    def contact_effect(self, other):
        self.health -= 1
        print(f"{self.name} bumps into {other.name}")

    def render(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )


@registry.register
class Sword(ContactInteractionMixin, GameObject):
    def __init__(self, x: int, y: int, name: str, health: int, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.color = (128, 0, 128)
        self.moving = False
        self.noise_intensity = 0.1
        self.attractiveness = 1.1
        self.visible_size = 0.5

    def contact_effect(self, other):
        if isinstance(other, Stone):
            self.health -= 3
            print(f"{self.name} dulls! Sharpness: {self.health}")

    def render(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )


@registry.register
class Elf(
    ContactInteractionMixin,
    BaseNPC,
    MovementMixin,
    SpeechMixin,
    LimbControlMixin,
    SightSensorMixin,
    HearingSensorMixin,
):
    def __init__(
        self,
        x: int,
        y: int,
        name: str,
        health: int,
        vision_range: int,
        hearing_range: int,
        **kwargs: Any,
    ):
        super().__init__(x, y, name, health, vision_range, hearing_range)
        self.color = (128, 0, 0)
        self.moving = False
        self.noise_intensity = 0.3
        self.attractiveness = 3.1
        self.visible_size = 2.3

    def contact_effect(self, other):
        if isinstance(other, Stone):
            self.health -= 2
            print("hit with stone")
        elif isinstance(other, Sword):
            self.health -= 4
            print("hit with sword")
        elif isinstance(other, HeatedStone):
            self.health -= 3
            print("hit with heated stone")

    def render(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )


@registry.register
class Cow(
    ContactInteractionMixin,
    BaseAnimal,
    MovementMixin,
    SpeechMixin,
    SightSensorMixin,
    HearingSensorMixin,
):
    def __init__(
        self,
        x: int,
        y: int,
        name: str,
        health: int,
        vision_range: int,
        hearing_range: int,
        **kwargs: Any,
    ):
        super().__init__(x, y, name, health, vision_range, hearing_range)
        self.color = (128, 255, 128)
        self.noise_intensity = 3.1
        self.attractiveness = 0.1
        self.visible_size = 4.0
        self.moving = False
        self.internal_state = InternalState(owner=self)

    def contact_effect(self, other):
        if isinstance(other, Stone):
            self.health -= 2
            print("hit with stone")
        elif isinstance(other, Sword):
            self.health -= 4
            print("hit with sword")
        elif isinstance(other, HeatedStone):
            self.health -= 3
            print("hit with heated stone")

    def render(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )


@registry.register
class Player(GameObject):
    def __init__(self, x: int, y: int, name: str, health: int, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.color = (0, 255, 0)
        self.noise_intensity = 1.1
        self.attractiveness = 2.1
        self.visible_size = 2.0

    def get_pressed_keys(self, keys) -> None:
        self.keys = keys

    def prepare(self, near_objs: Any):
        dx = dy = 0
        if self.keys[pygame.K_UP]:
            dy = -1
        elif self.keys[pygame.K_DOWN]:
            dy = 1
        elif self.keys[pygame.K_LEFT]:
            dx = -1
        elif self.keys[pygame.K_RIGHT]:
            dx = 1

        self.new_x = (self.x + dx) % MAX_X
        self.new_y = (self.y + dy) % MAX_Y

    def update(self, event):
        self.x = self.new_x
        self.y = self.new_y

    def render(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )
