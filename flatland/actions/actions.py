from typing import Literal, Optional

from ..consts import MAX_X, MAX_Y, Direction
from ..logger import Logger


class MovementMixin:
    logger = Logger()

    def move(self, direction: Direction):
        match direction:
            case Direction.DOWN:
                (dx, dy) = (0, 1)
            case Direction.UP:
                (dx, dy) = (0, -1)
            case Direction.RIGHT:
                (dx, dy) = (1, 0)
            case Direction.LEFT:
                (dx, dy) = (-1, 0)
        self.inertia = 1
        self.direction = direction
        self.x: int = (self.x + dx) % MAX_X
        self.y: int = (self.y + dy) % MAX_Y
        self.logger.info(f"{self.__class__.__name__} moves to ({self.x}, {self.y})")


class SpeechMixin:
    logger = Logger()

    def speak(self, message: Optional[str] = None):
        self.inertia = 0
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

    def grab(self):
        self.logger.info(f"{self.__class__.__name__} grabs.")

    def throw(self):
        self.logger.info(f"{self.__class__.__name__} throws.")
