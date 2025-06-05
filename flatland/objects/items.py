"""
----------------- Prototype pattern for all of the items below ---------------------
"""

from pathlib import Path
from typing import Any

import pygame

pygame.init()
pygame.display.set_mode((1, 1))

from ..actions.actions import LimbControlMixin, MovementMixin, SpeechMixin
from ..animations.animations import (
    AlwaysOnTopOfParent,
    MovementAnimationMixin,
    PushAnimationMixin,
    StandingAnimationMixin,
)
from ..consts import TILE_SIZE, Direction
from ..interactions.evolution import InertiaPrincipleWithFrictionEvolution
from ..interactions.interactions import (
    AttachedToParentMixin,
    ContactInteractionMixin,
    HeatInteractionMixin,
)
from ..internal.state import InternalState
from ..sensors.sensors import HearingSensorMixin, SightSensorMixin
from .base_objects import BaseAnimal, BaseNPC, GameObject
from .items_registry import registry


@registry.register
class Stone(
    ContactInteractionMixin,
    InertiaPrincipleWithFrictionEvolution,
    GameObject,
    MovementAnimationMixin,
    StandingAnimationMixin,
):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.color = (128, 128, 128)
        self.noise_intensity = 0.1
        self.attractiveness = 0.1
        self.visible_size = 0.5
        self.z_level = 1.0
        self.num_animations = 4  # do nnot forget this when inheriting from MovementAnimationMixin
        self.num_animations_standing = 1
        # Load sprites
        self.movement_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/boulder/up_{i}.png" for i in range(self.num_animations)
            ],
            Direction.DOWN: [
                f"assets/sprites/boulder/down_{i}.png" for i in range(self.num_animations)
            ],
            Direction.LEFT: [
                f"assets/sprites/boulder/left_{i}.png" for i in range(self.num_animations)
            ],
            Direction.RIGHT: [
                f"assets/sprites/boulder/right_{i}.png" for i in range(self.num_animations)
            ],
        }
        self.create_movement_sprites()  # do not forget!
        self.standing_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/boulder/up_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.DOWN: [
                f"assets/sprites/boulder/down_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.LEFT: [
                f"assets/sprites/boulder/left_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.RIGHT: [
                f"assets/sprites/boulder/right_{i}.png" for i in range(self.num_animations_standing)
            ],
        }

        self.create_standing_sprites()

    def render(self, screen: pygame.Surface) -> None:
        if self.x - self.prev_x != 0 or self.y - self.prev_y != 0:
            self.render_movement(screen)
        if self.x == self.prev_x and self.y == self.prev_y:
            self.render_standing(screen)


@registry.register
class Ground(GameObject):
    def __init__(self, x: int, y: int, name: str, health: float, tile_name: str, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.z_level = 0.0
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
    ContactInteractionMixin, HeatInteractionMixin, InertiaPrincipleWithFrictionEvolution, GameObject
):
    def __init__(
        self, x: int, y: int, name: str, health: float, temperature: float, **kwargs: Any
    ) -> None:
        super().__init__(x, y, name, health)
        self.temperature = temperature
        self.noise_intensity = 0.1
        self.attractiveness = 0.1
        self.visible_size = 0.5
        self.z_level = 1.0
        self.color = (255, 0, 0)

    def render(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )


@registry.register
class Sword(ContactInteractionMixin, GameObject, AttachedToParentMixin, AlwaysOnTopOfParent):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.color = (128, 0, 128)
        self.noise_intensity = 0.1
        self.attractiveness = 1.1
        self.z_level = 1.0
        self.visible_size = 0.5

    def render(self, screen):
        self.render_on_top()  # from AlwaysOnTopOfParent
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )


@registry.register
class Goblin(
    ContactInteractionMixin,
    BaseNPC,
    MovementMixin,
    SpeechMixin,
    LimbControlMixin,
    SightSensorMixin,
    HearingSensorMixin,
    PushAnimationMixin,
    MovementAnimationMixin,
    StandingAnimationMixin,
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
        self.z_level = 3.0
        self.num_animations = 6
        self.num_animations_push = 4
        self.num_animations_standing = 1

        # Load sprites
        self.movement_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/goblin/tile_2_{i}.png" for i in range(self.num_animations)
            ],
            Direction.DOWN: [
                f"assets/sprites/goblin/tile_0_{i}.png" for i in range(self.num_animations)
            ],
            Direction.LEFT: [
                f"assets/sprites/goblin/tile_3_{i}.png" for i in range(self.num_animations)
            ],
            Direction.RIGHT: [
                f"assets/sprites/goblin/tile_1_{i}.png" for i in range(self.num_animations)
            ],
        }
        self.create_movement_sprites()  # do not forget!
        self.standing_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/goblin/tile_2_{i+6}.png"
                for i in range(self.num_animations_standing)
            ],
            Direction.DOWN: [
                f"assets/sprites/goblin/tile_0_{i+6}.png"
                for i in range(self.num_animations_standing)
            ],
            Direction.LEFT: [
                f"assets/sprites/goblin/tile_3_{i+6}.png"
                for i in range(self.num_animations_standing)
            ],
            Direction.RIGHT: [
                f"assets/sprites/goblin/tile_1_{i+6}.png"
                for i in range(self.num_animations_standing)
            ],
        }
        self.create_standing_sprites()
        self.push_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/goblin/tile_2_{i+7}.png" for i in range(self.num_animations_push)
            ],
            Direction.DOWN: [
                f"assets/sprites/goblin/tile_0_{i+7}.png" for i in range(self.num_animations_push)
            ],
            Direction.LEFT: [
                f"assets/sprites/goblin/tile_3_{i+7}.png" for i in range(self.num_animations_push)
            ],
            Direction.RIGHT: [
                f"assets/sprites/goblin/tile_1_{i+7}.png" for i in range(self.num_animations_push)
            ],
        }
        self.create_push_sprites()

    def render(self, screen: pygame.Surface) -> None:
        if self.x - self.prev_x != 0 or self.y - self.prev_y != 0:
            self.render_movement(screen)
        elif (
            self.x == self.prev_x
            and self.y == self.prev_y
            and any("other" in kwargs for _, kwargs in self.volition.list_of_actions)
        ):
            self.render_push(screen)
        else:
            self.render_standing(screen)


@registry.register
class Cow(
    ContactInteractionMixin,
    BaseAnimal,
    MovementMixin,
    SpeechMixin,
    SightSensorMixin,
    HearingSensorMixin,
    InertiaPrincipleWithFrictionEvolution,
    MovementAnimationMixin,
    StandingAnimationMixin,
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
        self.num_animations_standing = 6
        self.z_level = 2.0
        self.sprite_size_x: int = 128
        self.sprite_size_y: int = 128

        # Load sprites
        self.movement_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/cow_move/up_{i}.png" for i in range(self.num_animations)
            ],
            Direction.DOWN: [
                f"assets/sprites/cow_move/down_{i}.png" for i in range(self.num_animations)
            ],
            Direction.LEFT: [
                f"assets/sprites/cow_move/left_{i}.png" for i in range(self.num_animations)
            ],
            Direction.RIGHT: [
                f"assets/sprites/cow_move/right_{i}.png" for i in range(self.num_animations)
            ],
        }
        self.create_movement_sprites()  # do not forget!
        self.standing_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/cow_eat/up_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.DOWN: [
                f"assets/sprites/cow_eat/down_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.LEFT: [
                f"assets/sprites/cow_eat/left_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.RIGHT: [
                f"assets/sprites/cow_eat/right_{i}.png" for i in range(self.num_animations_standing)
            ],
        }

        self.create_standing_sprites()

        # Load sound
        try:
            self.make_sound = pygame.mixer.Sound("assets/sounds/cow_moo.wav")
        except pygame.error:
            self.logger.info("Could not load sound. Probably mixer not initialised.")

    def render(self, screen: pygame.Surface) -> None:
        if self.x - self.prev_x != 0 or self.y - self.prev_y != 0:
            self.render_movement(
                screen
            )  # NOTE: here add all the rendering and respective interaction logics
        if self.x == self.prev_x and self.y == self.prev_y:
            self.render_standing(screen)


@registry.register
class CowShadow(GameObject, MovementAnimationMixin, AttachedToParentMixin):
    def __init__(self, x: int, y: int, name: str, health: int, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.z_level = 1
        self.num_animations = 1
        # Load sprites
        self.movement_sprites_locations = {
            Direction.UP: [f"assets/sprites/cow_shadow/up.png"],
            Direction.DOWN: [f"assets/sprites/cow_shadow/down.png"],
            Direction.LEFT: [f"assets/sprites/cow_shadow/left.png"],
            Direction.RIGHT: [f"assets/sprites/cow_shadow/right.png"],
        }
        self.create_movement_sprites()  # do not forget!
        self.sprite_size_x: int = 128
        self.sprite_size_y: int = 128

    def render(self, screen: pygame.Surface) -> None:
        self.render_movement(screen)


@registry.register
class Player(GameObject, LimbControlMixin):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.color = (0, 255, 0)
        self.noise_intensity = 1.1
        self.attractiveness = 2.1
        self.visible_size = 2.0
        self.z_level = 10.0

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
        elif self.keys[pygame.K_e]:
            for obj in near_objs:
                if obj.distance(self) < 1:
                    self.push(obj)
        match (dx, dy):
            case (1, 0):
                self.direction = Direction.RIGHT
            case (-1, 0):
                self.direction = Direction.LEFT
            case (0, 1):
                self.direction = Direction.DOWN
            case (0, -1):
                self.direction = Direction.UP

        self.new_x = self.x + dx
        self.new_y = self.y + dy

    def update(self, event):
        self.x = self.new_x
        self.y = self.new_y

    def render(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )
