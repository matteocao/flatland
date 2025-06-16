from typing import TYPE_CHECKING, Any, Literal, Optional

import pygame

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

    def slash(self: Any, other: "GameObject"):
        # stats check
        attk = sum([obj.attack for obj in self.children]) + self.attack
        dfnc = sum([obj.defence for obj in other.children]) + other.defence
        other.health -= max(0, attk - dfnc)

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

    def cast_magic(self: Any, game: "Game", keys) -> None:
        letters = {pygame.K_a: "A", pygame.K_s: "S", pygame.K_d: "D", pygame.K_f: "F"}

        numbers = {
            pygame.K_1: "1",
            pygame.K_2: "2",
            pygame.K_3: "3",
            pygame.K_4: "4",
            pygame.K_5: "5",
            pygame.K_6: "6",
            pygame.K_7: "7",
            pygame.K_8: "8",
            pygame.K_9: "9",
            pygame.K_0: "0",
        }

        for l_key, l_name in letters.items():
            for n_key, n_name in numbers.items():
                if keys[l_key] and keys[n_key]:
                    match (l_name, n_name):
                        case ("A", "1"):
                            print("A + 1 pressed")
                        case ("A", "2"):
                            print("A + 2 pressed")
                        case ("A", "3"):
                            print("A + 3 pressed")
                        case ("A", "4"):
                            print("A + 4 pressed")
                        case ("A", "5"):
                            print("A + 5 pressed")
                        case ("A", "6"):
                            print("A + 6 pressed")
                        case ("A", "7"):
                            print("A + 7 pressed")
                        case ("A", "8"):
                            print("A + 8 pressed")
                        case ("A", "9"):
                            print("A + 9 pressed")
                        case ("A", "0"):
                            print("A + 0 pressed")

                        case ("S", "1"):
                            print("S + 1 pressed")
                        case ("S", "2"):
                            print("S + 2 pressed")
                        case ("S", "3"):
                            print("S + 3 pressed")
                        case ("S", "4"):
                            print("S + 4 pressed")
                        case ("S", "5"):
                            print("S + 5 pressed")
                        case ("S", "6"):
                            print("S + 6 pressed")
                        case ("S", "7"):
                            print("S + 7 pressed")
                        case ("S", "8"):
                            print("S + 8 pressed")
                        case ("S", "9"):
                            print("S + 9 pressed")
                        case ("S", "0"):
                            print("S + 0 pressed")

                        case ("D", "1"):
                            print("D + 1 pressed")
                        case ("D", "2"):
                            print("D + 2 pressed")
                        case ("D", "3"):
                            print("D + 3 pressed")
                        case ("D", "4"):
                            print("D + 4 pressed")
                        case ("D", "5"):
                            print("D + 5 pressed")
                        case ("D", "6"):
                            print("D + 6 pressed")
                        case ("D", "7"):
                            print("D + 7 pressed")
                        case ("D", "8"):
                            print("D + 8 pressed")
                        case ("D", "9"):
                            print("D + 9 pressed")
                        case ("D", "0"):
                            print("D + 0 pressed")

                        case ("F", "1"):
                            magic = registry.create(
                                cls_name="FireBall",
                                x=self.x,
                                y=self.y,
                                name="fireball",
                                health=5,
                            )
                            magic.direction = self.direction
                        case ("F", "2"):
                            print("F + 2 pressed")
                        case ("F", "3"):
                            print("F + 3 pressed")
                        case ("F", "4"):
                            print("F + 4 pressed")
                        case ("F", "5"):
                            print("F + 5 pressed")
                        case ("F", "6"):
                            print("F + 6 pressed")
                        case ("F", "7"):
                            print("F + 7 pressed")
                        case ("F", "8"):
                            print("F + 8 pressed")
                        case ("F", "9"):
                            print("F + 9 pressed")
                        case ("F", "0"):
                            print("F + 0 pressed")
        game.current_level.register(magic)
        game.current_level.get_ground_objs(game)

    def push(self: Any, other: "GameObject") -> None:
        # stats check
        attk = sum([obj.attack for obj in self.children]) + self.attack
        dfnc = sum([obj.defence for obj in other.children]) + other.defence
        other.inertia += max(0, attk - dfnc)
        other.direction = self.direction
        self.logger.info(f"{self.__class__.__name__} pushes {other.__class__.__name__}.")
