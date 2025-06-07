"""
world
"""

from typing import TYPE_CHECKING, Any

from ..consts import MAX_X, MAX_Y
from ..logger import Logger

if TYPE_CHECKING:
    from ..objects.base_objects import GameObject


# --------------------- implemented via observer pattern ----------------
class World:
    """
    The world, treated as a subject to which all objects register to.
    Via the observer method, the world loops through the objects and updates them.
    """

    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any):
        if cls._instance is None:
            cls._instance = super(World, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_observers"):
            self._observers: list["GameObject"] = []
        self.logger = Logger()

    def register(self, obj: "GameObject") -> None:
        if obj not in self._observers:
            self.logger.info(f"Register to world {obj}")
            self._observers.append(obj)

    def send_keys_to_user(self, keys) -> None:
        for observer in self._observers:
            if hasattr(observer, "get_pressed_keys"):
                observer.get_pressed_keys(keys)

    def unregister(self, obj: "GameObject") -> None:
        if obj in self._observers:
            self._observers.remove(obj)

    def update(self, event: Any) -> None:
        for observer in self._observers:
            observer.update(event)

    def prepare(self, near_objs: Any) -> None:
        for obj in self._observers:
            obj.prepare(near_objs)

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


world = World()
