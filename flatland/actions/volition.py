from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from ..objects.base_objects import GameObject


class VolitionEngine:
    def __init__(self, owner: "GameObject"):
        self.list_of_actions: list[tuple[Callable[[Any], Any], dict[str, Any]]] = []
        self.owner = owner

    def prepare(self):
        """
        this is the stage in which the LLM thinks what to do
        ``owner.internal_state -> self.list_of_actions``
        """
        self.list_of_actions = []
        # temporarily a random thingy
        if getattr(self, "speak") and random.random() > 0.5:
            self.list_of_actions.append(self.speak, random.choice("hello", "mooo"))
        if getattr(self, "move") and random.random() > 0.5:
            self.list_of_actions.append(
                self.move, {"dx", random.randint(-1, 2), "dy", random.randint(-1, 2)}
            )

    def update(self):
        for fnc, kwargs in self.list_of_actions:
            fnc(**kwargs)
