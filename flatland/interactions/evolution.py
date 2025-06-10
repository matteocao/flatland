"""
The evolution mixin takes care of evolving an object that finds itself in a state that
is out of equilibrium, e.g. having non zero inertia (given that we assume friction)
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable

from ..consts import Direction
from ..logger import Logger
from .interactions import InteractionMixin

if TYPE_CHECKING:
    from ..objects.base_objects import GameObject


class InertiaPrincipleWithFrictionEvolution(InteractionMixin):
    def keep_on_moving(self):
        if getattr(self, "inertia", 0) <= 0.1:
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
        # NOTE: this check is very important otherwise this function will be called once for every object in the area
        if self is other:
            return [lambda: self.keep_on_moving()]
        return []


class HealthDecreasesEvolution(InteractionMixin):
    """
    This mixing decreases health as time goes by. Used to remove spawned objects like an evocation.
    """

    def keep_on_decreasing(self):
        if getattr(self, "health", 0) <= 0:
            return  # No decrease, death
        self.health -= 1

    def get_interaction_callables(self, other: "GameObject"):
        if self is other:
            return [lambda: self.keep_on_decreasing()]
        return []


class DamageHealthByTemperature(InteractionMixin):
    def damage_by_temperature(self: Any):
        if self.temperature > self.temperature_threshold_to_hurt_upper:
            self.health -= 1
        if self.temperature < self.temperature_threshold_to_hurt_lower:
            self.health -= 1
        self.temperature -= (
            self.temperature - self.equilibrium_temperature
        ) / 2  # decrease temperature

    def get_interaction_callables(self, other: "GameObject"):
        if self is other:
            return [lambda: self.damage_by_temperature()]
        return []


class DamageHealthByInertia(InteractionMixin):
    def damage_by_inertia(self: Any):
        if self.inertia > self.inertia_threshold_to_hurt:
            self.health -= 1.0
        self.inertia = max(0, self.inertia - 1.0)  # decrease inertia

    def get_interaction_callables(self, other: "GameObject"):
        if self is other:
            return [lambda: self.damage_by_inertia()]
        return []


class DeathMixin(InteractionMixin):
    def check_death(self):
        if hasattr(self, "health"):
            if self.health < 0.001:
                self.logger.info(f"{self.__class__.__name__} dies")
                from ..world.world import world

                world.unregister(self)

    def get_interaction_callables(self, other: "GameObject"):
        if self is other:
            return [lambda: self.check_death()]
        return []
