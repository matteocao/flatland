"""
----------------- Prototype pattern for all of the items below ---------------------
"""

from collections import defaultdict
from pathlib import Path
from typing import Any

import pygame

pygame.init()
pygame.display.set_mode((1, 1))

from ..actions.actions import LimbControlMixin, MovementMixin, SpeechMixin
from ..animations.animations import (
    CastingAnimationMixin,
    DeathAnimationMixin,
    MovementAnimationMixin,
    PushAnimationMixin,
    StandingAnimationMixin,
)
from ..animations.render import RenderMixin
from ..consts import TILE_SIZE, Direction
from ..interactions.evolution import (
    DamageHealthByInertia,
    DamageHealthByTemperature,
    DeathMixin,
    HealthDecreasesEvolution,
    HeatDissipation,
    InertiaPrincipleWithFrictionEvolution,
    ParentDeathIDie,
)
from ..interactions.interactions import (
    ContactInteractionMixin,
    EncumbranceMixin,
    ExplodeAtTouch,
    ExtendedObjectMixin,
    HeatInteractionMixin,
)
from ..internal.state import InternalState
from ..sensors.sensors import HearingSensorMixin, SightSensorMixin
from .base_objects import BaseAnimal, BaseNPC, GameObject
from .items_registry import registry


@registry.register
class Portal(
    GameObject,
    StandingAnimationMixin,
    RenderMixin,
):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.friction_coefficient = 1
        self.noise_intensity = 0.8
        self.attractiveness = 1.1
        self.visible_size = 1.5
        self.z_level = 2.0
        self.mass = 4
        self.health = 200
        self.is_encumbrant = False
        self.num_animations_standing = 64
        self.sprite_size_x: int = 80
        self.sprite_size_y: int = 60
        self.is_grabbable = True
        self.level_key = ""
        self.exit_name = ""
        # Load sprites
        self.standing_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/portal_1/portal{i+1}.png"
                for i in range(self.num_animations_standing)
            ],
            Direction.DOWN: [
                f"assets/sprites/portal_1/portal{i+1}.png"
                for i in range(self.num_animations_standing)
            ],
            Direction.LEFT: [
                f"assets/sprites/portal_1/portal{i+1}.png"
                for i in range(self.num_animations_standing)
            ],
            Direction.RIGHT: [
                f"assets/sprites/portal_1/portal{i+1}.png"
                for i in range(self.num_animations_standing)
            ],
        }
        self.__post_init__()  # do not forget

    def enter_portal(self) -> None:
        pygame.event.post(
            pygame.event.Event(pygame.USEREVENT, code=(self.level_key, self.exit_name))
        )
