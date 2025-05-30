from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable

from ..consts import Direction
from ..logger import Logger

if TYPE_CHECKING:
    from ..objects.base_objects import GameObject


class InteractionMixin(ABC):
    logger = Logger()

    @abstractmethod
    def get_interaction_callables(self, other: "GameObject") -> list[Callable[[], None]]:
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


class InertiaPrincipleWithFriction(InteractionMixin):
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
        self.inertia = new_inertia

    def get_interaction_callables(self, other: "GameObject"):
        return [lambda: self.keep_on_moving()]


class ContactInteractionMixin(InteractionMixin):
    x: int
    y: int
    name: str
    health: float
    mass: float
    inertia: int

    def on_contact(self, other: "GameObject"):
        if (
            isinstance(other, ContactInteractionMixin)
            and other.distance(self) < 0.1
            and not self is other
        ):
            self.logger.info(f"{self.__class__.__name__} contacts {other.__class__.__name__}")
            self.contact_effect(other)

    def contact_effect(self, other: "GameObject"):
        # Simple elastic collision logic: exchange inertia based on mass
        if not hasattr(self, "inertia") or not hasattr(other, "inertia"):
            return

        tup1: tuple[float, int] = self.mass, self.inertia
        tup2: tuple[float, int] = other.mass, other.inertia
        m1, v1 = tup1
        m2, v2 = tup2

        # Use 1D elastic collision formulas
        new_v1 = int(((m1 - m2) / (m1 + m2)) * v1 + ((2 * m2) / (m1 + m2)) * v2)
        new_v2 = int(((2 * m1) / (m1 + m2)) * v1 + ((m2 - m1) / (m1 + m2)) * v2)

        self.logger.info(
            f"Collision! {self.name} (mass={m1}, inertia={v1}) ↔ {other.name} (mass={m2}, inertia={v2})"
        )

        # Apply new inertia (velocity)
        self.inertia = max(0, new_v1)
        other.inertia = max(0, new_v2)

        # Optional: apply a health penalty
        impulse = abs(v1 - v2) * min(m1, m2)
        damage = impulse * 0.1  # arbitrary scaling
        self.health -= damage
        other.health -= damage

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

    def get_interaction_callables(self, other: "GameObject"):
        if isinstance(other, ContactInteractionMixin):
            return [lambda: self.on_contact(other)]
        return []


class DeathMixin(InteractionMixin):
    def check_death(self):
        if hasattr(self, "health"):
            if health <= 0:
                self.logger.info(f"{self.__class__.__name__} dies")
                del self

    def get_interaction_callables(self, other: "GameObject"):
        return [lambda: self.check_death()]
        return []


class HeatInteractionMixin(InteractionMixin):
    def on_heat_transfer(self, other: "GameObject"):
        if (
            hasattr(self, "temperature")
            and hasattr(other, "temperature")
            and other.distance(self) < 0.1
            and not self is other
        ):
            diff = (self.temperature - other.temperature) / 2
            self.temperature -= diff
            other.temperature += diff
            self.logger.info(
                f"{self.__class__.__name__} transfers heat to {other.__class__.__name__}"
            )

    def get_interaction_callables(self, other: "GameObject"):
        if isinstance(other, HeatInteractionMixin):
            return [lambda: self.on_heat_transfer(other)]
        return []
