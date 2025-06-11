from typing import TYPE_CHECKING, Any, Literal, Optional

from ..consts import Direction
from ..logger import Logger

if TYPE_CHECKING:
    from ..objects.base_objects import GameObject
    from ..objects.items import Ground


class MovementMixin:
    logger = Logger()
    direction: Direction
    ground_objs_list: list["Ground"]

    def get_ground_objs(self):
        from ..world.world import world

        self.ground_objs_list: list["Ground"] = [
            obj for obj in world._observers if obj.__class__.__name__ == "Ground"
        ]

    def move(self, direction: Direction):
        if self.direction == direction:
            match direction:
                case Direction.DOWN:
                    (dx, dy) = (0, 1)
                case Direction.UP:
                    (dx, dy) = (0, -1)
                case Direction.RIGHT:
                    (dx, dy) = (1, 0)
                case Direction.LEFT:
                    (dx, dy) = (-1, 0)
            try:
                grd = [
                    ground
                    for ground in self.ground_objs_list
                    if ground.x == self.x + dx and ground.y == self.y + dy
                ][0]
            except IndexError:
                self.logger.info(f"{self.__class__.__name__} cannot move outside ground")
                return
            if grd.is_walkable:
                self.x: int = self.x + dx
                self.y: int = self.y + dy
                self.logger.info(f"{self.__class__.__name__} moves to ({self.x}, {self.y})")
            else:
                self.logger.info(
                    f"{self.__class__.__name__} cannot walk to ({self.x+dx}, {self.y+dy})"
                )
        else:
            self.direction = direction


class SpeechMixin:
    logger = Logger()

    def speak(self, message: Optional[str] = None):
        if message:
            self.speech = message
        if hasattr(self, "make_sound"):
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

    def grab(self: Any, other: "GameObject"):
        if other.is_grabbable:
            self.children.append(other)
            other.parent = self
            other.x = self.x
            other.y = self.y
            other.direction = self.direction
            other.actions_per_second = self.actions_per_second
            other.scheduler.interval = 0.1

    def cast_magic(self):
        from ..objects.items_registry import registry
        from ..world.world import world

        fireball = registry.create(
            cls_name="FireBall",
            x=self.x,
            y=self.y,
            name="fireball",
            health=5,
        )
        fireball.direction = self.direction
        world.register(fireball)

    def push(self: Any, other: "GameObject") -> None:
        other.inertia += 2
        other.direction = self.direction
        self.logger.info(f"{self.__class__.__name__} pushes {other.__class__.__name__}.")
