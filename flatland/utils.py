from typing import Any, Generic, Iterator, TypeVar

from .consts import Direction


def move_in(self: Any, direction: Direction) -> bool:
    match direction:
        case Direction.DOWN:
            (dx, dy) = (0, 1)
        case Direction.UP:
            (dx, dy) = (0, -1)
        case Direction.RIGHT:
            (dx, dy) = (1, 0)
        case Direction.LEFT:
            (dx, dy) = (-1, 0)
    try:
        grd = [
            ground
            for ground in self.ground_objs_list
            if ground.x == self.x + dx and ground.y == self.y + dy
        ][0]
    except IndexError:
        self.logger.info(f"{self.__class__.__name__} cannot move outside ground")
        self.inertia = 0.0
        return False
    if grd.is_walkable or self.ignore_walkable:
        self.x = self.x + dx
        self.y = self.y + dy
        self.logger.info(f"{self.__class__.__name__} moves to ({self.x}, {self.y})")
        for (
            child
        ) in self.children:  # move all children that are locked to the parent in the same way
            if child.location_as_parent:
                child.x = self.x
                child.y = self.y
                child.prev_x = self.prev_x
                child.prev_y = self.prev_y
                child.direction = self.direction
                child.is_moving = True
        return True
    else:
        self.logger.info(f"{self.__class__.__name__} cannot walk to ({self.x+dx}, {self.y+dy})")
        return False


T = TypeVar("T")


class IdentitySetList(Generic[T]):
    def __init__(self) -> None:
        self._list: list[T] = []
        self._ids: set[int] = set()

    def append(self, item) -> None:
        obj_id = id(item)
        if obj_id not in self._ids:
            self._list.append(item)
            self._ids.add(obj_id)

    def __iter__(self) -> Iterator[T]:
        return iter(self._list)

    def __len__(self) -> int:
        return len(self._list)

    def __getitem__(self, index: int) -> T:
        return self._list[index]

    def clear(self) -> None:
        self._list.clear()
        self._ids = set()

    def __repr__(self) -> str:
        return str(self._list)

    def remove(self, item: T) -> None:
        obj_id = id(item)
        if obj_id in self._ids:
            self._ids.remove(obj_id)
            # Find the item by identity and remove it from the list
            for i, existing_item in enumerate(self._list):
                if existing_item is item:
                    del self._list[i]
                    break
