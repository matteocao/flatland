from typing import Optional


class MovementMixin:
    def move(self, dx: int, dy: int, world):
        self.x: int = (self.x + dx) % world.width
        self.y: int = (self.y + dy) % world.height
        print(f"{self.__class__.__name__} moves to ({self.x}, {self.y})")


class SpeechMixin:
    def speak(self, message: Optional[str] = None):
        default = getattr(
            self, "default_sound", f"{self.__class__.__name__} is silent."
        )
        print(f"{self.__class__.__name__} says: {message or default}")


class LimbControlMixin:
    def move_limbs(self, speed: float):
        if speed > 5:
            print(f"{self.__class__.__name__} punches!")
        elif speed > 0:
            print(f"{self.__class__.__name__} waves.")
        else:
            print(f"{self.__class__.__name__} does nothing.")

    def grab(self):
        print(f"{self.__class__.__name__} grabs.")

    def throw(self):
        print(f"{self.__class__.__name__} throws.")
