from typing import Optional

from ..consts import MAX_X, MAX_Y, Direction
from ..logger import Logger


class MovementMixin:
    logger = Logger()

    def move(self, dx: int, dy: int):
        try:
            # make sure we are not moving diagonally
            assert (dx, dy) in {(0, 1), (1, 0), (-1, 0), (0, -1)}, f"Movement error, got {(dx, dy)}"
            match (dx, dy):
                case (0, 1):
                    self.direction = Direction.DOWN
                    self.speed = 1
                case (0, -1):
                    self.direction = Direction.UP
                    self.speed = 1
                case (1, 0):
                    self.direction = Direction.RIGHT
                    self.speed = 1
                case (-1, 0):
                    self.direction = Direction.LEFT
                    self.speed = 1
            self.x: int = (self.x + dx) % MAX_X
            self.y: int = (self.y + dy) % MAX_Y
            self.logger.info(f"{self.__class__.__name__} moves to ({self.x}, {self.y})")
        except AssertionError as e:
            self.logger.info(e)
            self.speed = 0


class SpeechMixin:
    logger = Logger()

    def speak(self, message: Optional[str] = None):
        default = getattr(self, "default_sound", f"{self.__class__.__name__} is silent.")
        self.logger.info(f"{self.__class__.__name__} says: {message or default}")
        if hasattr(self, "moo_sound"):
            self.moo_sound.play()


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
