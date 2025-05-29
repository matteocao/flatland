import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .command import InteractionCommand


class InteractionScheduler:
    def __init__(self, interval: float = 1.0):
        self.queue: list["InteractionCommand"] = []
        self.last_execution = time.time()
        self.interval = interval

    def add(self, command: "InteractionCommand") -> None:
        self.queue.append(command)

    def update(self) -> None:
        current_time = time.time()
        if current_time - self.last_execution >= self.interval:
            for command in self.queue:
                command.execute()
            self.queue.clear()
            self.last_execution = current_time
