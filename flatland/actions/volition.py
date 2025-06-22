import random
from typing import TYPE_CHECKING, Any, Callable

import pygame

from ..consts import Direction
from ..logger import Logger

if TYPE_CHECKING:
    from ..internal.representation import ObjectRepresentation
    from ..objects.base_objects import GameObject


class VolitionEngine:

    def __init__(self, owner: "GameObject"):
        self.list_of_actions: list[tuple[Callable[[Any], Any], dict[str, Any]]] = []
        self.owner = owner
        self.logger = Logger()

    def _object_is_in_front(self, rep: "ObjectRepresentation"):
        if rep.dx is not None and rep.dy is not None:
            match self.owner.direction:
                case Direction.UP:
                    if abs(rep.dx) < 1 and 0 >= rep.dy >= -1:
                        return True
                case Direction.DOWN:
                    if abs(rep.dx) < 1 and 0 <= rep.dy <= 1:
                        return True
                case Direction.LEFT:
                    if abs(rep.dy) < 1 and 0 >= rep.dx >= -1:
                        return True
                case Direction.RIGHT:
                    if abs(rep.dy) < 1 and 0 <= rep.dx <= 1:
                        return True

            return False

    def prepare(self, game):
        """
        this is the stage in which the LLM thinks what to do
        ``owner.internal_state -> self.list_of_actions``
        """
        self.list_of_actions = []

        # check if this is the player
        if hasattr(self.owner, "get_pressed_keys"):
            if self.owner.keys:
                if self.owner.keys[pygame.K_UP]:
                    self.list_of_actions.append((self.owner.move, {"direction": Direction.UP}))
                elif self.owner.keys[pygame.K_DOWN]:
                    self.list_of_actions.append((self.owner.move, {"direction": Direction.DOWN}))
                elif self.owner.keys[pygame.K_LEFT]:
                    self.list_of_actions.append((self.owner.move, {"direction": Direction.LEFT}))
                elif self.owner.keys[pygame.K_RIGHT]:
                    self.list_of_actions.append((self.owner.move, {"direction": Direction.RIGHT}))
                elif self.owner.keys[pygame.K_e]:
                    for rep in self.owner.internal_state.latest_perception():
                        if abs(rep.dx) < 1 and abs(rep.dy) < 1 or self._object_is_in_front(rep):
                            self.list_of_actions.append(
                                (self.owner.push, {"other": rep.source_object})
                            )
                elif self.owner.keys[pygame.K_SPACE]:
                    for rep in self.owner.internal_state.latest_perception():
                        if abs(rep.dx) < 1 and abs(rep.dy) < 1 or self._object_is_in_front(rep):
                            self.list_of_actions.append(
                                (self.owner.slash, {"other": rep.source_object})
                            )
                elif self.owner.keys[pygame.K_q]:
                    for rep in self.owner.internal_state.latest_perception():
                        if abs(rep.dx) < 1 and abs(rep.dy) < 1:
                            self.list_of_actions.append(
                                (self.owner.grab, {"other": rep.source_object, "game": game})
                            )
                elif any(
                    [
                        self.owner.keys[key]
                        for key in {pygame.K_f, pygame.K_a, pygame.K_s, pygame.K_d}
                    ]
                ) and any(
                    [
                        self.owner.keys[key]
                        for key in {
                            pygame.K_1,
                            pygame.K_2,
                            pygame.K_3,
                            pygame.K_4,
                            pygame.K_5,
                            pygame.K_6,
                            pygame.K_7,
                            pygame.K_8,
                            pygame.K_9,
                            pygame.K_0,
                        }
                    ]
                ):
                    self.list_of_actions.append(
                        (self.owner.cast_magic, {"game": game, "keys": self.owner.keys})
                    )
                self.owner.keys = None
                self.owner.is_accepting_keys = True
        # temporarily a random thingy=
        elif hasattr(self.owner, "speak") and random.random() > 0.9:
            self.list_of_actions.append(
                (self.owner.speak, {"message": random.choice(self.owner.messages), "game": game})
            )
        elif hasattr(self.owner, "move") and random.random() > 0.5:
            self.list_of_actions.append(
                (
                    self.owner.move,
                    {
                        "direction": random.choice(
                            [Direction.DOWN, Direction.UP, Direction.LEFT, Direction.RIGHT]
                        )
                    },
                )
            )
        elif hasattr(self.owner, "push") and random.random() > 0.5:
            if self.owner.internal_state.time_history:
                try:
                    self.list_of_actions.append(
                        (
                            self.owner.push,
                            {
                                "other": random.choice(
                                    [
                                        rep.source_object
                                        for rep in self.owner.internal_state.latest_perception()
                                        if abs(rep.dx) < 1
                                        and abs(rep.dy) < 1
                                        or self._object_is_in_front(rep)
                                    ]
                                )
                            },
                        )
                    )
                except IndexError:
                    pass

    def update(self):
        for fnc, kwargs in self.list_of_actions:
            fnc(**kwargs)
