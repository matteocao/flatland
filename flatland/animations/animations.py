from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Literal,
    Optional,
    Protocol,
    TypeVar,
    no_type_check,
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
    location_as_parent: bool
    is_parent_animated_before: bool


class MovementAnimationMixin:
    """
    This is a very complex function, as it has to work properly online and on single player.
    The logic is to get the least amount of items from teh server, that may make the animation lag.
    The idea is to check if the last time this function was called, the target positions are the same or changed.
    This is the reason for the variables `last_x, last_y` and `x, y`.
    However, an additional complexity comes from all teh objects that should be bounded to stay attached to an object.
    Especially in multiplayer, we cannot rely on the server: hence, we propose here to overwrite the parameters of the
    children with those of the parent.
    A final complexity comes from the fact that the parent may have entered the movement mixin before or after the children,
    thus creating a "positional tick" of difference that may be very disturbing. To solve this, we try to estimate who passed
    first through this mixin.
    """

    movement_sprites_locations: dict[Direction, list[str]]
    animation_index: int = 0
    movement_sprites: dict[Direction, Any]
    alpha: float = 0.0
    last_x: int = 0
    last_y: int = 0
    is_parent_animated_before: bool = True
    x: int
    prev_x: int
    y: int
    prev_y: int

    def create_movement_sprites(self: HasMovementAttributes) -> None:
        self.movement_sprites = {
            k: list(map(lambda x: pygame.image.load(x).convert_alpha(), lst_str))
            for k, lst_str in self.movement_sprites_locations.items()
        }

    def update_movement_animation(self: HasMovementAttributes):
        self.animation_index = (self.animation_index + 1) % len(
            self.movement_sprites[self.direction]
        )

    @no_type_check
    def render_movement(self: HasMovementAttributes, screen: pygame.Surface) -> None:
        now = pygame.time.get_ticks()
        d_alpha = 0.11 * self.actions_per_second
        # conditions
        is_same_destination = self.last_x == self.x and self.y == self.last_y
        is_parent_auth = (
            self.location_as_parent
            and self.parent is not None
            and isinstance(self.parent, MovementAnimationMixin)
        )
        if is_parent_auth:
            # first we need to see if we have to reset the parent alpha
            if not (self.parent.last_x == self.parent.x and self.parent.y == self.parent.last_y):
                self.parent.alpha = 0.0
                self.parent.last_x = self.parent.x
                self.parent.last_y = self.parent.y
                self.is_parent_animated_before = False
            if self.parent.alpha > 1:
                self.is_parent_animated_before = True
            if self.is_parent_animated_before:
                self.alpha = self.parent.alpha - self.parent.actions_per_second * 0.11
            else:
                self.alpha = self.parent.alpha
            self.x = self.parent.x
            self.y = self.parent.y
            self.prev_x = self.parent.prev_x
            self.prev_y = self.parent.prev_y

        elif not is_same_destination:
            self.alpha = 0.0
            self.last_x = self.x
            self.last_y = self.y

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
