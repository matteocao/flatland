from typing import TYPE_CHECKING, Any, Literal, Optional

from ..consts import Direction
from ..logger import Logger
from ..objects.items_registry import registry
from ..utils import move_in

if TYPE_CHECKING:
    from ..game import Game
    from ..objects.base_objects import GameObject
    from ..objects.items import Ground


class MovementMixin:
    direction: Direction
    ground_objs_list: list["Ground"]

    def get_ground_objs(self, game: "Game") -> None:

        self.ground_objs_list: list["Ground"] = [
            obj for obj in game.current_level._observers if obj.__class__.__name__ == "Ground"  # type: ignore
        ]

    def move(self: Any, direction: Direction) -> None:
        if self.direction == direction:
            move_in(self, direction)
        else:
            self.direction = direction
            for (
                child
            ) in self.children:  # move all children that are locked to the parent in the same way
                if child.location_as_parent:
                    child.direction = direction


class SpeechMixin:
    volume: float

    def set_volume(self, player: "GameObject") -> None:
        self.volume = 1 / (1 + player.distance(self) ** 2)

    def speak(self: Any, message: Optional[str] = None) -> None:
        if message:
            self.speech = message
        if hasattr(self, "make_sound") and self.make_sound is not None:
            self.make_sound.set_volume(self.volume)
            self.make_sound.play()


class LimbControlMixin:
    logger = Logger()

    def move_limbs(self, speed: float):
        if speed > 5:
            self.logger.info(f"{self.__class__.__name__} punches!")
        elif speed > 0:
            self.logger.info(f"{self.__class__.__name__} waves.")
        else:
            self.logger.info(f"{self.__class__.__name__} does nothing.")

    def grab(self: Any, other: "GameObject") -> None:
        if other.is_grabbable:
            if hasattr(other, "enter_portal"):
                other.enter_portal()
                return
            self.children.append(other)
            other.parent = self
            other.x = self.x
            other.y = self.y
            other.direction = self.direction
            other.actions_per_second = self.actions_per_second
            other.scheduler.interval = self.scheduler.interval
            if other.render_on_top_of_parent:
                other.z_level = self.z_level + 1.0

    def cast_magic(self: Any, game: "Game") -> None:
        fireball = registry.create(
            cls_name="FireBall",
            x=self.x,
            y=self.y,
            name="fireball",
            health=5,
        )
        fireball.direction = self.direction
        game.current_level.register(fireball)
        game.current_level.get_ground_objs(game)

    def push(self: Any, other: "GameObject") -> None:
        other.inertia += 2
        other.direction = self.direction
        self.logger.info(f"{self.__class__.__name__} pushes {other.__class__.__name__}.")
