from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Literal,
    Optional,
    Protocol,
    TypeVar,
    runtime_checkable,
)

import pygame

from ..consts import TILE_SIZE, Direction
from ..logger import Logger

if TYPE_CHECKING:
    from ..objects.base_objects import GameObject

T = TypeVar("T", bound="Any[StandingAnimationMixin, GameObject]")


@runtime_checkable
class HasMovementAttributes(Protocol):
    actions_per_second: int
    x: int
    prev_x: int
    y: int
    prev_y: int
    direction: Direction
    movement_sprites_locations: dict[Direction, list[str]]
    animation_index: int
    movement_sprites: dict[Direction, Any]
    update_movement_animation: Callable[[], None]
    parent: "GameObject"
    sprite_size_x: int
    sprite_size_y: int
    alpha: float
    last_x: int
    last_y: int


class MovementAnimationMixin:
    movement_sprites_locations: dict[Direction, list[str]]
    animation_index: int = 0
    movement_sprites: dict[Direction, Any]
    alpha: float = 0.0
    last_x: int = 0
    last_y: int = 0

    def create_movement_sprites(self: HasMovementAttributes) -> None:
        self.movement_sprites = {
            k: list(map(lambda x: pygame.image.load(x).convert_alpha(), lst_str))
            for k, lst_str in self.movement_sprites_locations.items()
        }

    def update_movement_animation(self: HasMovementAttributes):
        self.animation_index = (self.animation_index + 1) % len(
            self.movement_sprites[self.direction]
        )

    def render_movement(self: HasMovementAttributes, screen: pygame.Surface) -> None:
        now = pygame.time.get_ticks()
        d_alpha = 0.1 * self.actions_per_second
        is_same_destination = self.last_x == self.x and self.y == self.last_y
        if not is_same_destination:
            self.alpha = 0.0
            self.last_x = self.x
            self.last_y = self.y

        # if self.has_just_started_moving:
        #    self.alpha = 0.0
        #    self.has_just_started_moving = False
        # alpha = (self.last_render_time - self.new_render_time) / 1000 * self.actions_per_second

        offset_x = self.sprite_size_x // 2 - TILE_SIZE // 2
        offset_y = self.sprite_size_y // 2 - TILE_SIZE // 2
        pos = (
            (self.alpha * self.x + (1 - self.alpha) * self.prev_x) * TILE_SIZE - offset_x,
            (self.alpha * self.y + (1 - self.alpha) * self.prev_y) * TILE_SIZE - offset_y,
        )
        self.update_movement_animation()
        sprite = self.movement_sprites[self.direction][self.animation_index]
        # TODO: here we will need to generalize with new animations and improve the logic
        screen.blit(sprite, pos)
        self.alpha = self.alpha + d_alpha


class StandingAnimationMixin:
    standing_sprites_locations: dict[Direction, list[str]]
    standing_animation_index: int = 0
    standing_sprites: dict[Direction, Any]

    def create_standing_sprites(self: T) -> None:
        self.standing_sprites = {
            k: list(map(lambda x: pygame.image.load(x).convert_alpha(), lst_str))
            for k, lst_str in self.standing_sprites_locations.items()
        }

    def update_standing_animation(self: T) -> None:
        self.standing_animation_index = (self.standing_animation_index + 1) % len(
            self.standing_sprites[self.direction]
        )

    def render_standing(self: T, screen: pygame.Surface) -> None:
        offset_x = self.sprite_size_x // 2 - TILE_SIZE // 2
        offset_y = self.sprite_size_y // 2 - TILE_SIZE // 2
        pos = (self.x * TILE_SIZE - offset_x, self.y * TILE_SIZE - offset_y)
        self.update_standing_animation()
        sprite = self.standing_sprites[self.direction][self.standing_animation_index]
        # TODO: here we will need to generalize with new animations and improve the logic
        screen.blit(sprite, pos)


class DeathAnimationMixin:
    dying_sprites_locations: dict[Direction, list[str]]
    dying_animation_index: int = 0
    dying_sprites: dict[Direction, Any]

    def create_dying_sprites(self: Any) -> None:
        self.dying_sprites = {
            k: list(map(lambda x: pygame.image.load(x).convert_alpha(), lst_str))
            for k, lst_str in self.dying_sprites_locations.items()
        }

    def update_dying_animation(self: Any):
        self.dying_animation_index = min(
            self.dying_animation_index + 1, len(self.dying_sprites[self.direction]) - 1
        )

    def render_dying(self: Any, screen: pygame.Surface) -> None:
        offset_x = self.sprite_size_x // 2 - TILE_SIZE // 2
        offset_y = self.sprite_size_y // 2 - TILE_SIZE // 2
        pos = (self.x * TILE_SIZE - offset_x, self.y * TILE_SIZE - offset_y)
        self.update_dying_animation()
        sprite = self.dying_sprites[self.direction][self.dying_animation_index]
        # TODO: here we will need to generalize with new animations and improve the logic
        screen.blit(sprite, pos)


class PushAnimationMixin:
    push_sprites_locations: dict[Direction, list[str]]
    push_animation_index: int = 0
    push_sprites: dict[Direction, Any]

    def create_push_sprites(self: Any) -> None:
        self.push_sprites = {
            k: list(map(lambda x: pygame.image.load(x).convert_alpha(), lst_str))
            for k, lst_str in self.push_sprites_locations.items()
        }

    def update_push_animation(self: Any):
        self.push_animation_index = (self.push_animation_index + 1) % len(
            self.push_sprites[self.direction]
        )

    def render_push(self: Any, screen: pygame.Surface) -> None:
        offset_x = self.sprite_size_x // 2 - TILE_SIZE // 2
        offset_y = self.sprite_size_y // 2 - TILE_SIZE // 2
        pos = (self.x * TILE_SIZE - offset_x, self.y * TILE_SIZE - offset_y)
        self.update_push_animation()
        sprite = self.push_sprites[self.direction][self.push_animation_index]
        # TODO: here we will need to generalize with new animations and improve the logic
        screen.blit(sprite, pos)


class AlwaysOnTopOfParent:
    """
    Mixin to be used in case you want an object to always be on top of the parent object, like an armor or helmet
    """

    def render_on_top(self: Any) -> None:
        if self.parent:
            self.z_level = self.parent.z_level + 1
