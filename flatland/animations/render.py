from typing import Any

import pygame


class RenderMixin:
    def render(self: Any, screen: pygame.Surface) -> None:
        if hasattr(self, "render_dying"):
            if self.health < 0.01:
                self.render_dying(screen)
                return
        if hasattr(self, "render_movement"):
            if self.is_moving:
                self.render_movement(screen)
                return
        if hasattr(self, "render_push"):
            if self.is_pushing:
                self.render_push(screen)
                return
        if hasattr(self, "render_standing"):
            if self.is_standing:
                self.render_standing(screen)
                return
        if hasattr(self, "render_casting"):
            if self.is_casting:
                self.render_casting(screen)
                return
        # fallback
        self.render_standing(screen)
