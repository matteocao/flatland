from typing import Any

import pygame

from ..actions.actions import MovementMixin, SpeechMixin
from ..consts import TILE_SIZE
from ..interactions.interactions import ContactInteractionMixin
from ..internal_representation.internal_state import InternalState
from .base_objects import BaseAnimal, BaseNPC, GameObject
from .items_registry import registry


@registry.register
class Stone(ContactInteractionMixin, GameObject):
    def __init__(self, x: int, y: int, name: str, health: int, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.color = (128, 128, 128)
        self.moving = False

    def contact_effect(self, other):
        if isinstance(other, Sword):
            self.health -= 2
            print(f"{self.name} chips! Durability: {self.health}")

    def update(self):
        pass

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

    def contact_effect(self, other):
        if isinstance(other, Stone):
            self.health -= 3
            print(f"{self.name} dulls! Sharpness: {self.health}")

    def update(self):
        pass

    def render(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )


@registry.register
class Man(ContactInteractionMixin, GameObject, MovementMixin, SpeechMixin):
    def __init__(self, x: int, y: int, name: str, health: int, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.color = (128, 0, 0)
        self.moving = False

    def contact_effect(self, other):
        if isinstance(other, Stone):
            self.health -= 3
            print(f"{self.name} dulls! Sharpness: {self.health}")

    def update(self):
        pass

    def render(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )


@registry.register
class Cow(ContactInteractionMixin, BaseAnimal, MovementMixin, SpeechMixin):
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
        self.moving = False
        self.internal_state = InternalState(owner=self)

    def update(self):
        self.internal_state.update(world.objects)
        for r in self.internal_state.latest_perception():
            print(
                f"Animal perceives {r.source_object.__class__.__name__} at dx={r.dx}, dy={r.dy}"
            )

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
class Player(GameObject):
    def __init__(self, x: int, y: int, name: str, health: int, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.color = (0, 255, 0)

    def handle_input(self, keys, max_x, max_y, objects):
        dx = dy = 0
        if keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_DOWN]:
            dy = 1
        elif keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_RIGHT]:
            dx = 1

        new_x = (self.x + dx) % max_x
        new_y = (self.y + dy) % max_y

        blocked = False
        for obj in objects:
            if obj.x == new_x and obj.y == new_y:
                if isinstance(obj, Stone):
                    obj.x = (obj.x + dx) % max_x
                    obj.y = (obj.y + dy) % max_y
                    obj.moving = True
                else:
                    blocked = True

        if not blocked:
            self.x = new_x
            self.y = new_y

    def update(self):
        pass

    def render(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )
