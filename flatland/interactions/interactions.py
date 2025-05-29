from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..objects.base_objects import GameObject


class InteractionMixin(ABC):
    @abstractmethod
    def execute_interaction(self, other: "GameObject") -> None:
        pass


class ContactInteractionMixin(InteractionMixin):
    def on_contact(self, other: "GameObject"):
        if isinstance(other, ContactInteractionMixin):
            print(f"{self.__class__.__name__} contacts {other.__class__.__name__}")
            self.contact_effect(other)

    def contact_effect(self, other: "GameObject"):
        pass  # override in subclass

    def execute_interaction(self, other: "GameObject") -> None:
        """
        Entry point for Command-style scheduling.
        This can be queued and called by a central scheduler.
        """
        self.on_contact(other)
