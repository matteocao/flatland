"""
The evolution mixin takes care of evolving an object that finds itself in a state that
is out of equilibrium, e.g. having non zero inertia (given that we assume friction)
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable

from ..consts import Direction
from ..logger import Logger
from .interactions import InteractionMixin

if TYPE_CHECKING:
    from ..objects.base_objects import GameObject


class InertiaPrincipleWithFrictionEvolution(InteractionMixin):
    def keep_on_moving(self):
        if getattr(self, "inertia", 0) <= 0:
            return  # No movement

        # Move in the current direction
        match self.direction:
            case Direction.UP:
                self.y -= 1
            case Direction.DOWN:
                self.y += 1
            case Direction.LEFT:
                self.x -= 1
            case Direction.RIGHT:
                self.x += 1

        # Apply friction
        new_inertia = max(0, self.inertia - self.friction_coefficient)
        self.logger.info(
            f"{self.name} moves {self.direction.name}, inertia: {self.inertia:.2f} → {new_inertia:.2f}, "
            f"position: ({self.x}, {self.y})"
        )
        self.inertia = new_inertia  # this stabilises inertia till it does not move anymore

    def get_interaction_callables(self, other: "GameObject"):
        return [lambda: self.keep_on_moving()]
