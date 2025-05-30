import random
from typing import TYPE_CHECKING, Any, Callable

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
        # temporarily a random thingy
        if hasattr(self.owner, "speak") and random.random() > 0.9:
            self.list_of_actions.append(
                (self.owner.speak, {"message": random.choice(["hello", "mooo"])})
            )
        if hasattr(self.owner, "move") and random.random() > 0.5:
            self.list_of_actions.append(
                (self.owner.move, {"dx": random.randint(-1, 2), "dy": random.randint(-1, 2)})
            )

    def update(self):
        for fnc, kwargs in self.list_of_actions:
            fnc(**kwargs)
