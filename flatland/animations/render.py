from typing import Any

import pygame


class RenderMixin:
    def render(self: Any, screen: pygame.Surface) -> None:
        if hasattr(self, "render_on_top"):
            self.render_on_top()
        if hasattr(self, "render_movement"):
            if self.x - self.prev_x != 0 or self.y - self.prev_y != 0:
                self.render_movement(screen)
                return
        if hasattr(self, "render_push"):
            if (
                self.x == self.prev_x
                and self.y == self.prev_y
                and any("push" == func.__name__ for func, _ in self.volition.list_of_actions)
            ):
                self.render_push(screen)
                return
        if hasattr(self, "render_standing"):
            if (
                self.x == self.prev_x
                and self.y == self.prev_y
                # and len(self.volition.list_of_actions) == 0
            ):
                self.render_standing(screen)
                return
