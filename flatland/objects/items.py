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
    DamageHealthByTemperature,
    DamageHealthByInertia,
    HeatInteractionMixin,
    RenderMixin,
    DeathMixin,
    DeathAnimationMixin,
):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.friction_coefficient = 1
        self.noise_intensity = 0.1
        self.inertia_threshold_to_hurt_upper = 1
        self.attractiveness = 0.1
        self.visible_size = 0.5
        self.z_level = 1.0
        self.mass = 200
        self.health = 10
        self.is_encumbrant = True
        self.num_animations = 4  # do not forget this when inheriting from MovementAnimationMixin
        self.num_animations_standing = 1
        self.num_animations_dying = 8
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
        self.dying_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/boulder/rock_crumble_{i+1}.png"
                for i in range(self.num_animations_dying)
            ],
            Direction.DOWN: [
                f"assets/sprites/boulder/rock_crumble_{i+1}.png"
                for i in range(self.num_animations_dying)
            ],
            Direction.LEFT: [
                f"assets/sprites/boulder/rock_crumble_{i+1}.png"
                for i in range(self.num_animations_dying)
            ],
            Direction.RIGHT: [
                f"assets/sprites/boulder/rock_crumble_{i+1}.png"
                for i in range(self.num_animations_dying)
            ],
        }
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
        self.__post_init__()  # do not forget


@registry.register
class OrangeTreeOne(
    ContactInteractionMixin,
    GameObject,
    StandingAnimationMixin,
    DamageHealthByTemperature,
    HeatDissipation,
    DamageHealthByInertia,
    HeatInteractionMixin,
    RenderMixin,
    DeathMixin,
):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.friction_coefficient = 1
        self.noise_intensity = 0.1
        self.attractiveness = 0.1
        self.visible_size = 2.5
        self.z_level = 15.0
        self.mass = 200
        self.health = 20
        self.is_encumbrant = True
        self.num_animations_standing = 1
        self.sprite_size_x: int = 128
        self.sprite_size_y: int = 186
        # Load sprites
        self.standing_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/trees/orangetree_{i+1}.png"
                for i in range(self.num_animations_standing)
            ],
            Direction.DOWN: [
                f"assets/sprites/trees/orangetree_{i+1}.png"
                for i in range(self.num_animations_standing)
            ],
            Direction.LEFT: [
                f"assets/sprites/trees/orangetree_{i+1}.png"
                for i in range(self.num_animations_standing)
            ],
            Direction.RIGHT: [
                f"assets/sprites/trees/orangetree_{i+1}.png"
                for i in range(self.num_animations_standing)
            ],
        }
        self.__post_init__()  # do not forget


@registry.register
class FireBall(
    InertiaPrincipleWithFrictionEvolution,
    GameObject,
    MovementAnimationMixin,
    RenderMixin,
    DamageHealthByTemperature,
    HeatDissipation,
    DamageHealthByInertia,
    HeatInteractionMixin,
    DeathMixin,
    DeathAnimationMixin,
    ExplodeAtTouch,
):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.friction_coefficient = 0.0
        self.noise_intensity = 0.1
        self.attractiveness = 0.1
        self.temperature_threshold_to_hurt_lower = 500
        self.temperature_threshold_to_hurt_upper = 10000000
        self.inertia_threshold_to_hurt_lower = 1
        self.visible_size = 0.5
        self.temperature = 10000
        self.health = 1
        self.inertia = 2.0
        self.is_moving = True  # by design
        self.z_level = 1.0
        self.ignore_walkable = True
        self.num_animations = 16  # do nnot forget this when inheriting from MovementAnimationMixin
        self.num_animations_dying = 7
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
        self.dying_sprites_locations = {
            Direction.UP: [
                f"assets/sprites/explosion/tile_0_{i}.png" for i in range(self.num_animations_dying)
            ],
            Direction.DOWN: [
                f"assets/sprites/explosion/tile_0_{i}.png" for i in range(self.num_animations_dying)
            ],
            Direction.LEFT: [
                f"assets/sprites/explosion/tile_0_{i}.png" for i in range(self.num_animations_dying)
            ],
            Direction.RIGHT: [
                f"assets/sprites/explosion/tile_0_{i}.png" for i in range(self.num_animations_dying)
            ],
        }
        self.__post_init__()  # do not forget


@registry.register
class Ground(GameObject, StandingAnimationMixin, RenderMixin, EncumbranceMixin):
    def __init__(self, x: int, y: int, name: str, health: float, tile_name: str, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.z_level = 0.0
        self.tile_name = tile_name
        self.num_animations_standing = 1
        self.scheduler.interval = 0.01
        self.actions_per_second = 9  # should be high, more than the player at least
        self.is_walkable = True  # used for encumbrance

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
        self.__post_init__()  # do not forget


@registry.register
class RobeTorso(
    GameObject,
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
        self.location_as_parent = True  # just set this for objects to stick to parent
        self.actions_per_second = 6
        self.render_on_top_of_parent = True
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
        self.__post_init__()  # do not forget


@registry.register
class Shoes(
    GameObject,
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
        self.location_as_parent = True  # just set this for objects to stick to parent
        self.actions_per_second = 6
        self.render_on_top_of_parent = True
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
        self.__post_init__()  # do not forget


@registry.register
class Hood(
    GameObject,
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
        self.location_as_parent = True  # just set this for objects to stick to parent
        self.actions_per_second = 6
        self.render_on_top_of_parent = True
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
        self.__post_init__()  # do not forget


@registry.register
class Skirt(
    GameObject,
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
        self.location_as_parent = True  # just set this for objects to stick to parent
        self.num_animations_standing = 1
        self.actions_per_second = 6
        self.render_on_top_of_parent = True
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
        self.__post_init__()  # do not forget


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
    DamageHealthByTemperature,
    HeatDissipation,
    DamageHealthByInertia,
    HeatInteractionMixin,
    DeathMixin,
    InertiaPrincipleWithFrictionEvolution,
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
        self.friction_coefficient = 1.0
        self.noise_intensity = 0.3
        self.attractiveness = 0.1
        self.visible_size = 2.3
        self.z_level = 3.0
        self.num_animations = 6
        self.num_animations_push = 4
        self.num_animations_standing = 1
        self.inertia_threshold_to_hurt_upper = 2.0
        self.inertia_threshold_to_hurt_lower = -1.0

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
        self.__post_init__()  # do not forget


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
    DamageHealthByTemperature,
    HeatDissipation,
    DamageHealthByInertia,
    HeatInteractionMixin,
    RenderMixin,
    DeathMixin,
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
        self.noise_intensity = 3.1
        self.attractiveness = 0.6
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
        self.__post_init__()  # do not forget

        # Load sound
        try:
            self.make_sound = pygame.mixer.Sound("assets/sounds/cow_moo.wav")
        except pygame.error:
            self.logger.info("Could not load sound. Probably mixer not initialised.")


@registry.register
class CowShadow(
    GameObject,
    MovementAnimationMixin,
    RenderMixin,
    StandingAnimationMixin,
    ParentDeathIDie,
):
    def __init__(self, x: int, y: int, name: str, health: int, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.z_level = 1
        self.num_animations = 1
        # self.scheduler.interval = 0.1
        self.sprite_size_x: int = 128
        self.sprite_size_y: int = 128
        self.location_as_parent = True  # just set this for objects to stick to parent

        # Load sprites
        self.movement_sprites_locations = {
            Direction.UP: [f"assets/sprites/cow_shadow/up.png"],
            Direction.DOWN: [f"assets/sprites/cow_shadow/down.png"],
            Direction.LEFT: [f"assets/sprites/cow_shadow/left.png"],
            Direction.RIGHT: [f"assets/sprites/cow_shadow/right.png"],
        }
        self.standing_sprites_locations = {
            Direction.UP: [f"assets/sprites/cow_shadow/up.png"],
            Direction.DOWN: [f"assets/sprites/cow_shadow/down.png"],
            Direction.LEFT: [f"assets/sprites/cow_shadow/left.png"],
            Direction.RIGHT: [f"assets/sprites/cow_shadow/right.png"],
        }
        self.__post_init__()  # do not forget


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
        self.__post_init__()  # do not forget

    def get_pressed_keys(self, keys) -> None:
        self.keys = keys


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
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, code=self.level_key))
