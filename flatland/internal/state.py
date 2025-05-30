from typing import TYPE_CHECKING, Dict, List, Type

from .representation import ObjectRepresentation

if TYPE_CHECKING:
    from ..objects.base_objects import GameObject

from collections import deque


class InternalState:
    def __init__(self, owner: "GameObject", history_length: int = 10) -> None:
        self.owner = owner
        self.time_history: deque[List[ObjectRepresentation]] = deque(maxlen=history_length)

    def update(self, perceivable_objects: List["GameObject"]):
        snapshot: Dict[int, ObjectRepresentation] = {}

        if hasattr(self.owner, "sense_sight"):
            self.owner.sense_sight(perceivable_objects, snapshot)
        if hasattr(self.owner, "sense_hearing"):
            self.owner.sense_hearing(perceivable_objects, snapshot)

        self.time_history.append(list(snapshot.values()))

    def latest_perception(self) -> List[ObjectRepresentation]:
        return self.time_history[-1] if self.time_history else []

    def get_representation(self, obj, snapshot: Dict[int, ObjectRepresentation]):
        key = id(obj)
        if key not in snapshot:
            snapshot[key] = ObjectRepresentation(
                dx=obj.x - self.owner.x, dy=obj.y - self.owner.y, source_object=obj
            )
        return snapshot[key]
