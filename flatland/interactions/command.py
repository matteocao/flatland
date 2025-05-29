from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..objects.base_objects import GameObject


class InteractionCommand:
    def __init__(self, initiator: "GameObject", target: "GameObject"):
        self.initiator = initiator
        self.target = target

    def execute(self):
        self.initiator.execute_interaction(
            self.target
        )  # this method is guaranteed by base class
