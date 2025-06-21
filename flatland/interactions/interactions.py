"""
Interactions are computed at one time step and set the objects new state after the interaction.
The the evolutioners take care of evolving the system till a stable configuration: e.g. till inertia=0 due to friction.
"""

from abc import ABC, abstractmethod
from statistics import mean
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


class AllChildrenDeadMixin(InteractionMixin):

    def all_children_dead(self: Any, game: "Game"):
        # check if children has died
        for obj in self.children:
            if obj not in game.current_level._observers:
                self.children.remove(obj)
        if len(self.children) == 0:
            if hasattr(self, "trigger_event"):
                self.trigger_event(game)

    def get_interaction_callables(
        self, other: "GameObject", game: "Game"
    ) -> list[Callable[[], None]]:
        return [lambda: self.all_children_dead(game)]


class ExtendedObjectMixin(InteractionMixin):
    """
    This class is useful to handle extended objects. The `schema` describes which other game tiles are affected.
    The schema is a dict, where teh key is the direction of teh object, and the value is the list of (dx, dy, True/False)
    indicating the objects that are part of the extended object, starting from the main one and whether they are encumbrant or not.
    The behaviour of the schema is:
        - damaged and health are shared
        - encumbrance is shared
        - the schema may vary according to directions
    """

    schema: dict[Direction, list[tuple[int, int, bool]]]

    def affect_children(self: Any, other: "GameObject", j: int) -> None:
        # children positions and encumbrance
        dx, dy, other.is_encumbrant = self.schema[self.direction][j]
        other.x, other.y = self.x + dx, self.y + dy

        # children health
        mean_health = mean([c.health for c in self.children])
        self.health: float = mean_health
        for ob in self.children:
            ob.health = mean_health

    def get_interaction_callables(
        self: Any, other: "GameObject", game: "Game"
    ) -> list[Callable[[], None]]:
        for j, obj in enumerate(self.children):
            if obj is other:
                return [lambda: self.affect_children(other, j)]
        return []
