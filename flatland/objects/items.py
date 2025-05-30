"""
----------------- Prototype pattern for all of the items below ---------------------
"""

from pathlib import Path
from typing import Any

import pygame

pygame.init()
pygame.display.set_mode((1, 1))

from ..actions.actions import LimbControlMixin, MovementMixin, SpeechMixin
from ..consts import MAX_X, MAX_Y, TILE_SIZE, Direction
from ..interactions.interactions import (
    ContactInteractionMixin,
    HeatInteractionMixin,
    InertiaPrincipleWithFriction,
)
from ..internal.state import InternalState
from ..sensors.sensors import HearingSensorMixin, SightSensorMixin
from .base_objects import BaseAnimal, BaseNPC, GameObject
from .items_registry import registry


@registry.register
class Stone(ContactInteractionMixin, InertiaPrincipleWithFriction, GameObject):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.color = (128, 128, 128)
        self.noise_intensity = 0.1
        self.attractiveness = 0.1
        self.visible_size = 0.5

    def render(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )


@registry.register
class Ground(GameObject):
    def __init__(self, x: int, y: int, name: str, health: float, tile_name: str, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.tile_name = tile_name
        # Extract NSWE neighbor tuple from the last 4 components of the name
        parts = self.tile_name.split("_")
        try:
            self.nswe_neigh = tuple(int(n) for n in parts[-4:])
        except ValueError:
            raise ValueError(f"Tile name '{tile_name}' does not end with four numeric components")

    def render(self, screen):
        sprite = pygame.image.load(f"{self.tile_name}.png").convert_alpha()
        screen.blit(sprite, (self.x * TILE_SIZE, self.y * TILE_SIZE))


@registry.register
class HeatedStone(
    ContactInteractionMixin, HeatInteractionMixin, InertiaPrincipleWithFriction, GameObject
):
    def __init__(
        self, x: int, y: int, name: str, health: float, temperature: float, **kwargs: Any
    ) -> None:
        super().__init__(x, y, name, health)
        self.temperature = temperature
        self.noise_intensity = 0.1
        self.attractiveness = 0.1
        self.visible_size = 0.5
        self.color = (255, 0, 0)

    def render(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )


@registry.register
class Sword(ContactInteractionMixin, GameObject):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.color = (128, 0, 128)
        self.noise_intensity = 0.1
        self.attractiveness = 1.1
        self.visible_size = 0.5

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
        health: float,
        vision_range: int,
        hearing_range: int,
        **kwargs: Any,
    ):
        super().__init__(x, y, name, health, vision_range, hearing_range)
        self.color = (128, 0, 0)
        self.noise_intensity = 0.3
        self.attractiveness = 3.1
        self.visible_size = 2.3

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
        health: float,
        vision_range: int,
        hearing_range: int,
        **kwargs: Any,
    ):
        super().__init__(x, y, name, health, vision_range, hearing_range)
        self.color = (128, 255, 128)
        self.noise_intensity = 3.1
        self.attractiveness = 0.1
        self.visible_size = 4.0
        self.internal_state = InternalState(owner=self)
        self.num_animations = 4

        # Load sprites
        self.movement_sprites_locations = {
            Direction.UP: [f"assets/sprites/cow/up_{i}.png" for i in range(self.num_animations)],
            Direction.DOWN: [
                f"assets/sprites/cow/down_{i}.png" for i in range(self.num_animations)
            ],
            Direction.LEFT: [
                f"assets/sprites/cow/left_{i}.png" for i in range(self.num_animations)
            ],
            Direction.RIGHT: [
                f"assets/sprites/cow/right_{i}.png" for i in range(self.num_animations)
            ],
        }
        self.create_movement_sprites()  # do not forget!

        # Load sound
        try:
            self.make_sound = pygame.mixer.Sound("assets/sounds/cow_moo.wav")
        except pygame.error:
            self.logger.info("Could not load sound. Probably mixer not initialised.")


@registry.register
class Player(GameObject):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any):
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
