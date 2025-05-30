from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from ..objects.base_objects import GameObject


class InteractionMixin(ABC):
    @abstractmethod
    def get_interaction_callables(self, other: "GameObject") -> list[Callable[[], None]]:
        """Return list of interaction callables relevant for this mixin"""
        pass


class ContactInteractionMixin(InteractionMixin):
    def on_contact(self, other: "GameObject"):
        if (
            isinstance(other, ContactInteractionMixin)
            and other.distance(self) <= 1
            and not self is other
        ):
            print(f"{self.__class__.__name__} contacts {other.__class__.__name__}")
            self.contact_effect(other)

    def contact_effect(self, other: "GameObject"):
        raise NotImplementedError  # override in subclass

    def get_interaction_callables(self, other: "GameObject"):
        if isinstance(other, ContactInteractionMixin):
            return [lambda: self.on_contact(other)]
        return []


class DeathMixin(InteractionMixin):
    def check_death(self):
        if hasattr(self, "health"):
            if health <= 0:
                print(f"{self.__class__.__name__} dies")
                del self

    def get_interaction_callables(self, other: "GameObject"):
        return [lambda: self.check_death()]
        return []


class HeatInteractionMixin(InteractionMixin):
    def on_heat_transfer(self, other: "GameObject"):
        if (
            hasattr(self, "temperature")
            and hasattr(other, "temperature")
            and other.distance(self) < 1
            and not self is other
        ):
            diff = (self.temperature - other.temperature) / 2
            self.temperature -= diff
            other.temperature += diff
            print(f"{self.__class__.__name__} transfers heat to {other.__class__.__name__}")

    def get_interaction_callables(self, other: "GameObject"):
        if isinstance(other, HeatInteractionMixin):
            return [lambda: self.on_heat_transfer(other)]
        return []
