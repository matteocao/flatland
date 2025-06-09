from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from .command import InteractionCommand


class InteractionScheduler:
    def __init__(self, interval: float = 1.0):
        self.queue: list["InteractionCommand"] = []
        self.last_execution = pygame.time.get_ticks()
        self.interval = interval
        self.last_tick_up: int = 0

    def add(self, command: "InteractionCommand") -> None:
        self.queue.append(command)

    def update(self) -> None:
        tick = int(pygame.time.get_ticks() // (self.interval * 1000))
        if tick != self.last_tick_up:
            for command in self.queue:
                command.execute()
            self.queue.clear()
            self.last_tick_up = tick
