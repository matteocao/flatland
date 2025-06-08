import random
from typing import TYPE_CHECKING, Any, Callable

import pygame

from ..consts import Direction
from ..logger import Logger

if TYPE_CHECKING:
    from ..objects.base_objects import GameObject


class VolitionEngine:
    def __init__(self, owner: "GameObject"):
        self.list_of_actions: list[tuple[Callable[[Any], Any], dict[str, Any]]] = []
        self.owner = owner
        self.logger = Logger()

    def prepare(self):
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
                        if abs(rep.dx) < 1 and abs(rep.dy) < 1:
                            self.list_of_actions.append(
                                (self.owner.push, {"other": rep.source_object})
                            )
                elif self.owner.keys[pygame.K_q]:
                    for rep in self.owner.internal_state.latest_perception():
                        if abs(rep.dx) < 1 and abs(rep.dy) < 1:
                            self.list_of_actions.append(
                                (self.owner.grab, {"other": rep.source_object})
                            )
                elif self.owner.keys[pygame.K_SPACE]:
                    self.list_of_actions.append((self.owner.cast_magic, {}))
                self.owner.keys = None
        # temporarily a random thingy=
        elif hasattr(self.owner, "speak") and random.random() > 0.9:
            self.list_of_actions.append(
                (self.owner.speak, {"message": random.choice(["hello", "mooo"])})
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
                self.list_of_actions.append(
                    (
                        self.owner.push,
                        {
                            "other": random.choice(
                                [
                                    rep.source_object
                                    for rep in self.owner.internal_state.time_history[-1]
                                    if abs(rep.dx) < 1 and abs(rep.dy) < 1
                                ]
                            )
                        },
                    )
                )

    def update(self):
        for fnc, kwargs in self.list_of_actions:
            fnc(**kwargs)
