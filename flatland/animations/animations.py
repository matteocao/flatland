from typing import TYPE_CHECKING, Any, Callable, Literal, Optional, Protocol, runtime_checkable

import pygame

from ..consts import NEXT_ANIMATION_STEPS, TILE_SIZE, Direction
from ..logger import Logger

if TYPE_CHECKING:
    from ..objects.base_objects import GameObject


@runtime_checkable
class HasMovementAttributes(Protocol):
    movement_sprites_locations: dict[Direction, list[str]]
    is_update_just_done: bool
    actions_per_second: int
    x: int
    prev_x: int
    y: int
    prev_y: int
    direction: Direction
    animation_timer: int
    animation_index: int
    last_render_time: int
    new_render_time: int
    num_animations: int
    movement_sprites: dict[Direction, dict]
    update_movement_animation: Callable[[], None]
    parent: "GameObject"
    sprite_size_x: int
    sprite_size_y: int


class MovementAnimationMixin:
    logger = Logger()

    def create_movement_sprites(self: HasMovementAttributes | Any) -> None:
        self.movement_sprites = {
            k: list(map(lambda x: pygame.image.load(x).convert_alpha(), lst_str))
            for k, lst_str in self.movement_sprites_locations.items()
        }

    def update_movement_animation(self: HasMovementAttributes | Any):
        self.animation_timer += 1
        if self.animation_timer >= NEXT_ANIMATION_STEPS:
            self.animation_timer = 0
            self.animation_index = (self.animation_index + 1) % len(
                self.movement_sprites[self.direction]
            )

    def render_movement(self: HasMovementAttributes | Any, screen: pygame.Surface) -> None:
        now = pygame.time.get_ticks()
        if self.is_update_just_done:
            self.new_render_time = now
        self.last_render_time = now
        alpha = (self.last_render_time - self.new_render_time) / 1000 * self.actions_per_second
        offset_x = self.sprite_size_x // 2 - TILE_SIZE // 2
        offset_y = self.sprite_size_y // 2 - TILE_SIZE // 2
        pos = (
            (alpha * self.x + (1 - alpha) * self.prev_x) * TILE_SIZE - offset_x,
            (alpha * self.y + (1 - alpha) * self.prev_y) * TILE_SIZE - offset_y,
        )
        self.update_movement_animation()
        sprite = self.movement_sprites[self.direction][self.animation_index]
        # TODO: here we will need to generalize with new animations and improve the logic
        screen.blit(sprite, pos)


class StandingAnimationMixin:
    logger = Logger()

    def create_standing_sprites(self: Any) -> None:
        self.standing_sprites = {
            k: list(map(lambda x: pygame.image.load(x).convert_alpha(), lst_str))
            for k, lst_str in self.standing_sprites_locations.items()
        }

    def update_standing_animation(self: Any):
        self.standing_animation_timer += 1
        if self.standing_animation_timer >= NEXT_ANIMATION_STEPS:
            self.standing_animation_timer = 0
            self.standing_animation_index = (self.standing_animation_index + 1) % len(
                self.standing_sprites[self.direction]
            )

    def render_standing(self: Any, screen: pygame.Surface) -> None:
        now = pygame.time.get_ticks()
        if self.is_update_just_done:
            self.new_render_time = now
        self.last_render_time = now
        alpha = (self.last_render_time - self.new_render_time) / 1000 * self.actions_per_second
        offset_x = self.sprite_size_x // 2 - TILE_SIZE // 2
        offset_y = self.sprite_size_y // 2 - TILE_SIZE // 2
        pos = (self.x * TILE_SIZE - offset_x, self.y * TILE_SIZE - offset_y)
        self.update_standing_animation()
        sprite = self.standing_sprites[self.direction][self.standing_animation_index]
        # TODO: here we will need to generalize with new animations and improve the logic
        screen.blit(sprite, pos)


class AlwaysOnTopOfParent:
    """
    Mixin to be used in case you want an object to always be on top of the parent object, like an armor or helmet
    """

    def render_on_top(self: HasMovementAttributes | Any) -> None:
        if self.parent:
            self.z_level = self.parent.z_level + 1
