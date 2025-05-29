"""
world
"""

from typing import TYPE_CHECKING, Any

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

    def register(self, obj: "GameObject") -> None:
        if obj not in self._observers:
            self._observers.append(obj)

    def send_keys_to_user(self, keys) -> None:
        for observer in self._observers:
            if hasattr(observer, "get_pressed_keys"):
                observer.get_pressed_keys(keys)

    def unregister(self, obj: "GameObject") -> None:
        if obj in self._observers:
            self._observers.remove(obj)

    def update(self, event) -> None:
        for observer in self._observers:
            observer.update(event)

    def prepare(self, keys) -> None:
        for obj in self._observers:
            obj.prepare(keys)

    def render(self, screen) -> None:
        for obj in self._observers:
            obj.render(screen)


world = World()
