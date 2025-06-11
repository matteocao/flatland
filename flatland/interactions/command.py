from typing import TYPE_CHECKING

from .interactions import InteractionMixin

if TYPE_CHECKING:
    from ..__main__ import Game
    from ..objects.base_objects import GameObject


class InteractionCommand:
    def __init__(self, initiator: "GameObject", target: "GameObject", game: "Game"):
        self.initiator = initiator
        self.target = target
        self.game = game

    def execute(self):
        if isinstance(self.initiator, InteractionMixin):
            callables = []
            for base in self.initiator.__class__.__mro__:
                if issubclass(base, InteractionMixin) and base != InteractionMixin:
                    mixin_obj = base.__dict__.get("get_interaction_callables")
                    if mixin_obj:
                        calls = base.get_interaction_callables(
                            self.initiator, self.target, self.game
                        )
                        callables.extend(calls)
            for call in callables:
                call()
