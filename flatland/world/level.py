"""
world
"""

from typing import TYPE_CHECKING, Any

import pygame

from ..consts import MAX_X, MAX_Y
from ..logger import Logger

if TYPE_CHECKING:
    from ..__main__ import Game
    from ..objects.base_objects import GameObject
    from ..objects.items import Player


# --------------------- implemented via observer pattern ----------------
class Level:
    """
    The level, treated as a subject to which all objects register to.
    Via the observer method, the world loops through the objects and updates them.
    """

    def __init__(self, level_key: str = "") -> None:
        self._observers: list["GameObject"] = []
        self._scheduled_to_die: list[tuple["GameObject", int, int]] = []
        self.logger = Logger()
        self.level_key = level_key

    def register(self, obj: "GameObject") -> None:
        if obj not in self._observers:
            self.logger.info(f"Register to world {obj}")
            self._observers.append(obj)

    def send_keys_to_user(self, keys) -> None:
        for observer in self._observers:
            if hasattr(observer, "get_pressed_keys"):
                observer.get_pressed_keys(keys)

    def get_ground_objs(self, game: "Game"):
        """This is to allow movement"""
        for obj in self._observers:
            if hasattr(obj, "get_ground_objs"):
                obj.get_ground_objs(game)

    def unregister(self, obj: "GameObject") -> None:
        if obj in self._observers:
            self._observers.remove(obj)

    def set_volume(self, player: "Player") -> None:
        for obj in self._observers:
            if hasattr(obj, "set_volume"):
                obj.set_volume(player)

    def update(self, event: Any) -> None:
        for observer in self._observers:
            observer.update(event)
        now = pygame.time.get_ticks()
        for obj, dt, t in self._scheduled_to_die:
            if t + dt < now:
                self.unregister(obj)
                self._scheduled_to_die.remove((obj, dt, t))

    def prepare(self, near_objs: Any, game: "Game") -> None:
        for obj in self._observers:
            obj.prepare(near_objs, game)

    def reset_is_walkable(self) -> None:
        for observer in self._observers:
            if hasattr(observer, "reset_is_walkable"):
                observer.reset_is_walkable()

    def correct_periodic_positions(self) -> None:
        for obj in self._observers:
            obj.x = obj.x % MAX_X
            obj.y = obj.y % MAX_Y

    def render(self, screen) -> None:
        for obj in self.order_observers_by_z_level():
            if hasattr(obj, "render"):
                obj.render(screen)

    def order_observers_by_z_level(self) -> list["GameObject"]:
        return sorted(self._observers, key=lambda obj: obj.z_level)

    def schedule_to_unregister(self, obj, timer_ms: int = 1000) -> None:
        now = pygame.time.get_ticks()
        self._scheduled_to_die.append((obj, timer_ms, now))

    def extract_instance(self, obj_serial: dict[str, Any]) -> Any:
        for obj in self._observers:
            obj_state = self.get_obj_state(obj)
            if obj_serial == obj_state:
                return obj
        return None

    def get_serializable_state(self) -> dict[str, list[dict[str, Any]]]:
        """
        This method is needed in the multiplayer only, to serialise the objects and
        transfer them over the internet.
        """
        objs = []
        for obj in self._observers:
            obj_state = self.get_obj_state(obj)
            objs.append(obj_state)
        return {"objects": objs}

    def get_obj_state(self, obj: "GameObject") -> dict[str, Any]:
        obj_state = {
            "id": obj.id,
            "cls_name": obj.__class__.__name__,
            "x": obj.x,
            "y": obj.y,
            "health": obj.health,
            "name": obj.name,
            "tile_name": getattr(obj, "tile_name", None),
            "prev_x": obj.prev_x,
            "prev_y": obj.prev_y,
            "inertia": obj.inertia,
            "direction": obj.direction,
            "is_moving": obj.is_moving,
            "is_pushing": obj.is_pushing,
            "is_standing": obj.is_standing,
            "parent_id": obj.parent_id,
            "render_on_top_of_parent": obj.render_on_top_of_parent,
            "location_as_parent": obj.location_as_parent,
            "movement_sprites_locations": getattr(obj, "movement_sprites_locations", None),
            "standing_sprites_locations": getattr(obj, "standing_sprites_locations", None),
            "dying_sprites_locations": getattr(obj, "dying_sprites_locations", None),
            "push_sprites_locations": getattr(obj, "push_sprites_locations", None),
            "level_key": getattr(obj, "level_key", None),
            "volume": getattr(obj, "volume", None),
            "z_level": obj.z_level,
            "sprite_size_x": obj.sprite_size_x,
            "sprite_size_y": obj.sprite_size_y,
        }
        return obj_state
