from typing import Any, Callable, Literal, Optional, Protocol, runtime_checkable

import pygame

from ..consts import NEXT_ANIMATION_STEPS, TILE_SIZE, Direction
from ..logger import Logger


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


class MovementAnimationMixin:
    logger = Logger()

    def create_movement_sprites(self: HasMovementAttributes | Any) -> None:
        self.movement_sprites = {
            k: list(map(lambda x: pygame.image.load(x).convert_alpha(), lst_str))
            for k, lst_str in self.movement_sprites_locations.items()
        }

    def update_movement_animation(self: HasMovementAttributes | Any):
        if self.x - self.prev_x != 0 or self.y - self.prev_y != 0:
            self.animation_timer += 1
            if self.animation_timer >= NEXT_ANIMATION_STEPS:
                self.animation_timer = 0
                self.animation_index = (self.animation_index + 1) % len(
                    self.movement_sprites[self.direction]
                )
        else:
            self.animation_index = 0  # standing still

    def render_movement(self: HasMovementAttributes | Any, screen: pygame.Surface) -> None:
        now = pygame.time.get_ticks()
        if self.is_update_just_done:
            self.new_render_time = now
        self.last_render_time = now
        alpha = (self.last_render_time - self.new_render_time) / 1000 * self.actions_per_second
        pos = (
            (alpha * self.x + (1 - alpha) * self.prev_x) * TILE_SIZE,
            (alpha * self.y + (1 - alpha) * self.prev_y) * TILE_SIZE,
        )
        self.update_movement_animation()
        sprite = self.movement_sprites[self.direction][self.animation_index]
        # TODO: here we will need to generalize with new animations and improve the logic
        screen.blit(sprite, pos)
