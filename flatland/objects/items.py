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
    AlwaysOnTopOfParent,
    MovementAnimationMixin,
    PushAnimationMixin,
    StandingAnimationMixin,
)
from ..animations.render import RenderMixin
from ..consts import TILE_SIZE, Direction
from ..interactions.evolution import (
    DeathMixin,
    HealthDecreasesEvolution,
    InertiaPrincipleWithFrictionEvolution,
)
from ..interactions.interactions import (
    AttachedToParentMixin,
    ContactInteractionMixin,
    HeatInteractionMixin,
)
from ..internal.state import InternalState
from ..sensors.sensors import HearingSensorMixin, SightSensorMixin
from .base_objects import BaseAnimal, BaseNPC, GameObject
from .items_registry import registry


@registry.register
class Stone(
    ContactInteractionMixin,
    InertiaPrincipleWithFrictionEvolution,
    GameObject,
    MovementAnimationMixin,
    StandingAnimationMixin,
    RenderMixin,
):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.color = (128, 128, 128)
        self.noise_intensity = 0.1
        self.attractiveness = 0.1
        self.visible_size = 0.5
        self.z_level = 1.0
        self.num_animations = 4  # do nnot forget this when inheriting from MovementAnimationMixin
        self.num_animations_standing = 1
        # Load sprites
        self.movement_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/boulder/up_{i}.png" for i in range(self.num_animations)
            ],
            Direction.DOWN: [
                f"assets/sprites/boulder/down_{i}.png" for i in range(self.num_animations)
            ],
            Direction.LEFT: [
                f"assets/sprites/boulder/left_{i}.png" for i in range(self.num_animations)
            ],
            Direction.RIGHT: [
                f"assets/sprites/boulder/right_{i}.png" for i in range(self.num_animations)
            ],
        }
        self.create_movement_sprites()  # do not forget!
        self.standing_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/boulder/up_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.DOWN: [
                f"assets/sprites/boulder/down_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.LEFT: [
                f"assets/sprites/boulder/left_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.RIGHT: [
                f"assets/sprites/boulder/right_{i}.png" for i in range(self.num_animations_standing)
            ],
        }

        self.create_standing_sprites()


@registry.register
class FireBall(
    InertiaPrincipleWithFrictionEvolution,
    GameObject,
    MovementAnimationMixin,
    RenderMixin,
    HealthDecreasesEvolution,
    DeathMixin,
):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.friction_coefficient = 0
        self.noise_intensity = 0.1
        self.attractiveness = 0.1
        self.visible_size = 0.5
        self.inertia = 2
        self.z_level = 1.0
        self.num_animations = 16  # do nnot forget this when inheriting from MovementAnimationMixin
        # Load sprites
        self.movement_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/fireball/up_{i}.png" for i in range(self.num_animations)
            ],
            Direction.DOWN: [
                f"assets/sprites/fireball/down_{i}.png" for i in range(self.num_animations)
            ],
            Direction.LEFT: [
                f"assets/sprites/fireball/left_{i}.png" for i in range(self.num_animations)
            ],
            Direction.RIGHT: [
                f"assets/sprites/fireball/right_{i}.png" for i in range(self.num_animations)
            ],
        }
        self.create_movement_sprites()  # do not forget!


@registry.register
class Ground(GameObject, StandingAnimationMixin, RenderMixin):
    def __init__(self, x: int, y: int, name: str, health: float, tile_name: str, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.z_level = 0.0
        self.tile_name = tile_name
        self.num_animations_standing = 1
        # Extract NSWE neighbor tuple from the last 4 components of the name
        parts = self.tile_name.split("_")
        try:
            self.nswe_neigh = tuple(int(n) for n in parts[-4:])
        except ValueError:
            raise ValueError(f"Tile name '{tile_name}' does not end with four numeric components")
        self.standing_sprites_locations = {
            Direction.UP: [f"{self.tile_name}.png" for i in range(self.num_animations_standing)],
            Direction.DOWN: [f"{self.tile_name}.png" for i in range(self.num_animations_standing)],
            Direction.LEFT: [f"{self.tile_name}.png" for i in range(self.num_animations_standing)],
            Direction.RIGHT: [f"{self.tile_name}.png" for i in range(self.num_animations_standing)],
        }

        self.create_standing_sprites()


@registry.register
class RobeTorso(
    GameObject,
    AttachedToParentMixin,
    AlwaysOnTopOfParent,
    MovementAnimationMixin,
    StandingAnimationMixin,
    RenderMixin,
):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.noise_intensity = 0.1
        self.attractiveness = 1.1
        self.visible_size = 0.5
        self.num_animations = 8
        self.num_animations_standing = 1
        self.scheduler.interval = 0.1  # NOTE: needed to keep on top of the player
        self.is_grabbable = True

        # Load sprites
        self.movement_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/robe_torso/tile_0_{i+1}.png" for i in range(self.num_animations)
            ],
            Direction.DOWN: [
                f"assets/sprites/robe_torso/tile_2_{i+1}.png" for i in range(self.num_animations)
            ],
            Direction.LEFT: [
                f"assets/sprites/robe_torso/tile_1_{i+1}.png" for i in range(self.num_animations)
            ],
            Direction.RIGHT: [
                f"assets/sprites/robe_torso/tile_3_{i+1}.png" for i in range(self.num_animations)
            ],
        }
        self.create_movement_sprites()  # do not forget!
        self.standing_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/robe_torso/tile_0_{i}.png"
                for i in range(self.num_animations_standing)
            ],
            Direction.DOWN: [
                f"assets/sprites/robe_torso/tile_2_{i}.png"
                for i in range(self.num_animations_standing)
            ],
            Direction.LEFT: [
                f"assets/sprites/robe_torso/tile_1_{i}.png"
                for i in range(self.num_animations_standing)
            ],
            Direction.RIGHT: [
                f"assets/sprites/robe_torso/tile_3_{i}.png"
                for i in range(self.num_animations_standing)
            ],
        }

        self.create_standing_sprites()


@registry.register
class Shoes(
    GameObject,
    AttachedToParentMixin,
    AlwaysOnTopOfParent,
    MovementAnimationMixin,
    StandingAnimationMixin,
    RenderMixin,
):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.noise_intensity = 0.1
        self.attractiveness = 1.1
        self.visible_size = 0.5
        self.num_animations = 8
        self.num_animations_standing = 1
        self.scheduler.interval = 0.1  # NOTE: needed to keep on top of the player
        self.is_grabbable = True

        # Load sprites
        self.movement_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/shoes/tile_0_{i+1}.png" for i in range(self.num_animations)
            ],
            Direction.DOWN: [
                f"assets/sprites/shoes/tile_2_{i+1}.png" for i in range(self.num_animations)
            ],
            Direction.LEFT: [
                f"assets/sprites/shoes/tile_1_{i+1}.png" for i in range(self.num_animations)
            ],
            Direction.RIGHT: [
                f"assets/sprites/shoes/tile_3_{i+1}.png" for i in range(self.num_animations)
            ],
        }
        self.create_movement_sprites()  # do not forget!
        self.standing_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/shoes/tile_0_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.DOWN: [
                f"assets/sprites/shoes/tile_2_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.LEFT: [
                f"assets/sprites/shoes/tile_1_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.RIGHT: [
                f"assets/sprites/shoes/tile_3_{i}.png" for i in range(self.num_animations_standing)
            ],
        }

        self.create_standing_sprites()


@registry.register
class Hood(
    GameObject,
    AttachedToParentMixin,
    AlwaysOnTopOfParent,
    MovementAnimationMixin,
    StandingAnimationMixin,
    RenderMixin,
):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.noise_intensity = 0.1
        self.attractiveness = 1.1
        self.visible_size = 0.5
        self.num_animations = 8
        self.num_animations_standing = 1
        self.scheduler.interval = 0.1  # NOTE: needed to keep on top of the player
        self.is_grabbable = True

        # Load sprites
        self.movement_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/hood/tile_0_{i+1}.png" for i in range(self.num_animations)
            ],
            Direction.DOWN: [
                f"assets/sprites/hood/tile_2_{i+1}.png" for i in range(self.num_animations)
            ],
            Direction.LEFT: [
                f"assets/sprites/hood/tile_1_{i+1}.png" for i in range(self.num_animations)
            ],
            Direction.RIGHT: [
                f"assets/sprites/hood/tile_3_{i+1}.png" for i in range(self.num_animations)
            ],
        }
        self.create_movement_sprites()  # do not forget!
        self.standing_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/hood/tile_0_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.DOWN: [
                f"assets/sprites/hood/tile_2_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.LEFT: [
                f"assets/sprites/hood/tile_1_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.RIGHT: [
                f"assets/sprites/hood/tile_3_{i}.png" for i in range(self.num_animations_standing)
            ],
        }

        self.create_standing_sprites()


@registry.register
class Skirt(
    GameObject,
    AttachedToParentMixin,
    AlwaysOnTopOfParent,
    MovementAnimationMixin,
    StandingAnimationMixin,
    RenderMixin,
):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.noise_intensity = 0.1
        self.attractiveness = 1.1
        self.visible_size = 0.5
        self.num_animations = 8
        self.num_animations_standing = 1
        self.scheduler.interval = 0.1  # NOTE: needed to keep on top of the player
        self.is_grabbable = True

        # Load sprites
        self.movement_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/skirt/tile_0_{i+1}.png" for i in range(self.num_animations)
            ],
            Direction.DOWN: [
                f"assets/sprites/skirt/tile_2_{i+1}.png" for i in range(self.num_animations)
            ],
            Direction.LEFT: [
                f"assets/sprites/skirt/tile_1_{i+1}.png" for i in range(self.num_animations)
            ],
            Direction.RIGHT: [
                f"assets/sprites/skirt/tile_3_{i+1}.png" for i in range(self.num_animations)
            ],
        }
        self.create_movement_sprites()  # do not forget!
        self.standing_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/skirt/tile_0_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.DOWN: [
                f"assets/sprites/skirt/tile_2_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.LEFT: [
                f"assets/sprites/skirt/tile_1_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.RIGHT: [
                f"assets/sprites/skirt/tile_3_{i}.png" for i in range(self.num_animations_standing)
            ],
        }

        self.create_standing_sprites()


@registry.register
class Goblin(
    ContactInteractionMixin,
    BaseNPC,
    MovementMixin,
    SpeechMixin,
    LimbControlMixin,
    SightSensorMixin,
    HearingSensorMixin,
    PushAnimationMixin,
    MovementAnimationMixin,
    StandingAnimationMixin,
    RenderMixin,
):
    def __init__(
        self,
        x: int,
        y: int,
        name: str,
        health: float,
        vision_range: int,
        hearing_range: int,
        **kwargs: Any,
    ):
        super().__init__(x, y, name, health, vision_range, hearing_range)
        self.color = (128, 0, 0)
        self.noise_intensity = 0.3
        self.attractiveness = 0.1
        self.visible_size = 2.3
        self.z_level = 3.0
        self.num_animations = 6
        self.num_animations_push = 4
        self.num_animations_standing = 1

        # Load sprites
        self.movement_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/goblin/tile_2_{i}.png" for i in range(self.num_animations)
            ],
            Direction.DOWN: [
                f"assets/sprites/goblin/tile_0_{i}.png" for i in range(self.num_animations)
            ],
            Direction.LEFT: [
                f"assets/sprites/goblin/tile_3_{i}.png" for i in range(self.num_animations)
            ],
            Direction.RIGHT: [
                f"assets/sprites/goblin/tile_1_{i}.png" for i in range(self.num_animations)
            ],
        }
        self.create_movement_sprites()  # do not forget!
        self.standing_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/goblin/tile_2_{i+6}.png"
                for i in range(self.num_animations_standing)
            ],
            Direction.DOWN: [
                f"assets/sprites/goblin/tile_0_{i+6}.png"
                for i in range(self.num_animations_standing)
            ],
            Direction.LEFT: [
                f"assets/sprites/goblin/tile_3_{i+6}.png"
                for i in range(self.num_animations_standing)
            ],
            Direction.RIGHT: [
                f"assets/sprites/goblin/tile_1_{i+6}.png"
                for i in range(self.num_animations_standing)
            ],
        }
        self.create_standing_sprites()
        self.push_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/goblin/tile_2_{i+7}.png" for i in range(self.num_animations_push)
            ],
            Direction.DOWN: [
                f"assets/sprites/goblin/tile_0_{i+7}.png" for i in range(self.num_animations_push)
            ],
            Direction.LEFT: [
                f"assets/sprites/goblin/tile_3_{i+7}.png" for i in range(self.num_animations_push)
            ],
            Direction.RIGHT: [
                f"assets/sprites/goblin/tile_1_{i+7}.png" for i in range(self.num_animations_push)
            ],
        }
        self.create_push_sprites()


@registry.register
class Cow(
    ContactInteractionMixin,
    BaseAnimal,
    MovementMixin,
    SpeechMixin,
    SightSensorMixin,
    HearingSensorMixin,
    InertiaPrincipleWithFrictionEvolution,
    MovementAnimationMixin,
    StandingAnimationMixin,
    RenderMixin,
):
    def __init__(
        self,
        x: int,
        y: int,
        name: str,
        health: float,
        vision_range: int,
        hearing_range: int,
        **kwargs: Any,
    ):
        super().__init__(x, y, name, health, vision_range, hearing_range)
        self.color = (128, 255, 128)
        self.noise_intensity = 3.1
        self.attractiveness = 0.1
        self.visible_size = 4.0
        self.internal_state = InternalState(owner=self)
        self.num_animations = 4
        self.num_animations_standing = 6
        self.z_level = 2.0
        self.sprite_size_x: int = 128
        self.sprite_size_y: int = 128

        # Load sprites
        self.movement_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/cow_move/up_{i}.png" for i in range(self.num_animations)
            ],
            Direction.DOWN: [
                f"assets/sprites/cow_move/down_{i}.png" for i in range(self.num_animations)
            ],
            Direction.LEFT: [
                f"assets/sprites/cow_move/left_{i}.png" for i in range(self.num_animations)
            ],
            Direction.RIGHT: [
                f"assets/sprites/cow_move/right_{i}.png" for i in range(self.num_animations)
            ],
        }
        self.create_movement_sprites()  # do not forget!
        self.standing_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/cow_eat/up_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.DOWN: [
                f"assets/sprites/cow_eat/down_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.LEFT: [
                f"assets/sprites/cow_eat/left_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.RIGHT: [
                f"assets/sprites/cow_eat/right_{i}.png" for i in range(self.num_animations_standing)
            ],
        }

        self.create_standing_sprites()

        # Load sound
        try:
            self.make_sound = pygame.mixer.Sound("assets/sounds/cow_moo.wav")
        except pygame.error:
            self.logger.info("Could not load sound. Probably mixer not initialised.")


@registry.register
class CowShadow(GameObject, MovementAnimationMixin, AttachedToParentMixin, RenderMixin):
    def __init__(self, x: int, y: int, name: str, health: int, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.z_level = 1
        self.num_animations = 1
        self.scheduler.interval = 0.1
        # Load sprites
        self.movement_sprites_locations = {
            Direction.UP: [f"assets/sprites/cow_shadow/up.png"],
            Direction.DOWN: [f"assets/sprites/cow_shadow/down.png"],
            Direction.LEFT: [f"assets/sprites/cow_shadow/left.png"],
            Direction.RIGHT: [f"assets/sprites/cow_shadow/right.png"],
        }
        self.create_movement_sprites()  # do not forget!
        self.sprite_size_x: int = 128
        self.sprite_size_y: int = 128


@registry.register
class Player(
    BaseNPC,
    LimbControlMixin,
    MovementAnimationMixin,
    MovementMixin,
    StandingAnimationMixin,
    HearingSensorMixin,
    SightSensorMixin,
    RenderMixin,
):
    def __init__(
        self,
        x: int,
        y: int,
        name: str,
        health: float,
        vision_range: int,
        hearing_range: int,
        **kwargs: Any,
    ):
        super().__init__(x, y, name, health, vision_range, hearing_range)
        self.noise_intensity = 1.1
        self.attractiveness = 2.1
        self.visible_size = 2.0
        self.z_level = 10.0
        self.actions_per_second = 3
        self.keys = None
        self.num_animations = 8
        self.num_animations_standing = 1

        # Load sprites
        self.movement_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/man/tile_0_{i+1}.png" for i in range(self.num_animations)
            ],
            Direction.DOWN: [
                f"assets/sprites/man/tile_2_{i+1}.png" for i in range(self.num_animations)
            ],
            Direction.LEFT: [
                f"assets/sprites/man/tile_1_{i+1}.png" for i in range(self.num_animations)
            ],
            Direction.RIGHT: [
                f"assets/sprites/man/tile_3_{i+1}.png" for i in range(self.num_animations)
            ],
        }
        self.create_movement_sprites()  # do not forget!
        self.standing_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/man/tile_0_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.DOWN: [
                f"assets/sprites/man/tile_2_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.LEFT: [
                f"assets/sprites/man/tile_1_{i}.png" for i in range(self.num_animations_standing)
            ],
            Direction.RIGHT: [
                f"assets/sprites/man/tile_3_{i}.png" for i in range(self.num_animations_standing)
            ],
        }

        self.create_standing_sprites()

    def get_pressed_keys(self, keys) -> None:
        self.keys = keys
