"""
Interactions are computed at one time step and set the objects new state after the interaction.
The the evolutioners take care of evolving the system till a stable configuration: e.g. till inertia=0 due to friction.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable

from ..consts import Direction
from ..logger import Logger

if TYPE_CHECKING:
    from ..game import Game
    from ..objects.base_objects import GameObject


class InteractionMixin(ABC):
    logger = Logger()

    @abstractmethod
    def get_interaction_callables(
        self, other: "GameObject", game: "Game"
    ) -> list[Callable[[], None]]:
        """Return list of interaction callables relevant for this mixin"""
        pass

    @staticmethod
    def reverse_direction(direction: Direction) -> Direction:
        return {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }.get(direction, direction)


class EncumbranceMixin(InteractionMixin):
    """
    This mixin prevent movements in the location of self. This has to be attached to the Ground objects.
    """

    def reset_is_walkable(self) -> None:
        self.is_walkable = True

    def prevent_movement(self: Any, other) -> None:
        if self.distance(other) < 1 and other.is_encumbrant:
            self.is_walkable = False

    def get_interaction_callables(
        self: Any, other: "GameObject", game: "Game"
    ) -> list[Callable[[], None]]:
        if other.__class__.__name__ != "Ground":
            return [lambda: self.prevent_movement(other)]
        return []


class ContactInteractionMixin(InteractionMixin):
    """
    This mixin takes care of collisions. This does not affect health, only inertia and directions.
    """

    inertia: float

    def on_contact(self: Any, other: "GameObject") -> None:
        if (
            isinstance(other, ContactInteractionMixin)
            and other.distance(self) < 0.1
            and not self is other
        ):
            self.logger.info(f"{self.__class__.__name__} contacts {other.__class__.__name__}")
            self.contact_effect(other)

    def contact_effect(self: Any, other: "GameObject") -> None:
        # Simple elastic collision logic: exchange inertia based on mass

        tup1: tuple[float, float] = self.mass, self.inertia
        tup2: tuple[float, float] = other.mass, other.inertia
        m1, v1 = tup1
        m2, v2 = tup2

        # Use 1D linear formulas
        self.inertia = abs((m1 * v1 + m2 * v2) / (m1 + m2))
        other.inertia = abs((m1 * v1 + m2 * v2) / (m1 + m2))

        self.logger.info(
            f"Collision! {self.name} (mass={m1}, inertia={v1}) ↔ {other.name} (mass={m2}, inertia={v2})"
        )

        # 🔄 Update directions
        if v1 > 0 and v2 > 0:
            # Both moving → reverse directions
            self.direction: Direction = self.reverse_direction(self.direction)
            other.direction = self.reverse_direction(other.direction)
        elif v1 == 0 and v2 > 0:
            self.direction = other.direction
        elif v2 == 0 and v1 > 0:
            other.direction = self.direction
        # then the inertia mixin will take care of movement.

        self.logger.info(
            f"{self.name} new inertia: {self.inertia:.2f}, health: {self.health:.1f} | "
            f"{other.name} new inertia: {other.inertia:.2f}, health: {other.health:.1f}"
        )

    def get_interaction_callables(
        self, other: "GameObject", game: "Game"
    ) -> list[Callable[[], None]]:
        if isinstance(other, ContactInteractionMixin):
            return [lambda: self.on_contact(other)]
        return []


class ExplodeAtTouch(InteractionMixin):
    health: float
    inertia: float

    def explode(self, other: "GameObject"):
        if (
            isinstance(other, HeatInteractionMixin)
            and other.distance(self) < 0.1
            and not self is other
        ):
            self.health = 0
            self.inertia = 0

    def get_interaction_callables(
        self, other: "GameObject", game: "Game"
    ) -> list[Callable[[], None]]:
        if isinstance(other, HeatInteractionMixin):
            return [lambda: self.explode(other)]
        return []


class HeatInteractionMixin(InteractionMixin):
    temperature: float

    def on_heat_transfer(self: Any, other: "GameObject"):
        if (
            isinstance(other, HeatInteractionMixin)
            and other.distance(self) < 0.1
            and not self is other
        ):
            avg_temp = (self.temperature * self.mass + other.temperature * other.mass) / (
                self.mass + other.mass
            )
            self.temperature = avg_temp
            other.temperature = avg_temp
            self.logger.info(
                f"{self.__class__.__name__} transfers heat to {other.__class__.__name__}"
            )

    def get_interaction_callables(
        self, other: "GameObject", game: "Game"
    ) -> list[Callable[[], None]]:
        if isinstance(other, HeatInteractionMixin):
            return [lambda: self.on_heat_transfer(other)]
        return []
