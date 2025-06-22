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
from ..consts import BLACK, TILE_SIZE, WHITE, Direction
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
    AllChildrenDeadMixin,
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
        self.standing_sprites_locations = [
            {
                Direction.UP: [
                    f"assets/sprites/boulder/up_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.DOWN: [
                    f"assets/sprites/boulder/down_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.LEFT: [
                    f"assets/sprites/boulder/left_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.RIGHT: [
                    f"assets/sprites/boulder/right_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
            }
        ]
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
        self.standing_sprites_locations = [
            {
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
        ]
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
        self.standing_sprites_locations = [
            {
                Direction.UP: [
                    f"{self.tile_name}.png" for i in range(self.num_animations_standing)
                ],
                Direction.DOWN: [
                    f"{self.tile_name}.png" for i in range(self.num_animations_standing)
                ],
                Direction.LEFT: [
                    f"{self.tile_name}.png" for i in range(self.num_animations_standing)
                ],
                Direction.RIGHT: [
                    f"{self.tile_name}.png" for i in range(self.num_animations_standing)
                ],
            }
        ]
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
        self.standing_sprites_locations = [
            {
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
        ]
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
        self.standing_sprites_locations = [
            {
                Direction.UP: [
                    f"assets/sprites/shoes/tile_0_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.DOWN: [
                    f"assets/sprites/shoes/tile_2_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.LEFT: [
                    f"assets/sprites/shoes/tile_1_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.RIGHT: [
                    f"assets/sprites/shoes/tile_3_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
            }
        ]
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
        self.standing_sprites_locations = [
            {
                Direction.UP: [
                    f"assets/sprites/hood/tile_0_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.DOWN: [
                    f"assets/sprites/hood/tile_2_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.LEFT: [
                    f"assets/sprites/hood/tile_1_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.RIGHT: [
                    f"assets/sprites/hood/tile_3_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
            }
        ]
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
        self.standing_sprites_locations = [
            {
                Direction.UP: [
                    f"assets/sprites/skirt/tile_0_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.DOWN: [
                    f"assets/sprites/skirt/tile_2_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.LEFT: [
                    f"assets/sprites/skirt/tile_1_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.RIGHT: [
                    f"assets/sprites/skirt/tile_3_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
            }
        ]
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
        self.messages = ["Hello!!", "I am going\nto trick you!"]

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
        self.standing_sprites_locations = [
            {
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
        ]
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
        self.messages = ["Mooo"]

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
        self.standing_sprites_locations = [
            {
                Direction.UP: [
                    f"assets/sprites/cow_eat/up_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.DOWN: [
                    f"assets/sprites/cow_eat/down_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.LEFT: [
                    f"assets/sprites/cow_eat/left_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.RIGHT: [
                    f"assets/sprites/cow_eat/right_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
            }
        ]
        self.__post_init__()  # do not forget

        # Load sound
        try:
            self.make_sound = pygame.mixer.Sound("assets/sounds/cow_moo.wav")
        except pygame.error:
            self.logger.info("Could not load sound. Probably mixer not initialised.")
            self.make_sound = None  # type: ignore


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
        self.standing_sprites_locations = [
            {
                Direction.UP: [f"assets/sprites/cow_shadow/up.png"],
                Direction.DOWN: [f"assets/sprites/cow_shadow/down.png"],
                Direction.LEFT: [f"assets/sprites/cow_shadow/left.png"],
                Direction.RIGHT: [f"assets/sprites/cow_shadow/right.png"],
            }
        ]
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
        self.is_accepting_keys = True

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
        self.standing_sprites_locations = [
            {
                Direction.UP: [
                    f"assets/sprites/man/tile_0_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.DOWN: [
                    f"assets/sprites/man/tile_2_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.LEFT: [
                    f"assets/sprites/man/tile_1_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.RIGHT: [
                    f"assets/sprites/man/tile_3_{i}.png"
                    for i in range(self.num_animations_standing)
                ],
            }
        ]
        self.__post_init__()  # do not forget

    def get_pressed_keys(self, keys) -> None:
        if self.is_accepting_keys:
            self.keys = keys
            if any(self.keys):  # type: ignore
                self.is_accepting_keys = False
            else:
                self.is_accepting_keys = True


@registry.register
class HouseOneMain(
    ContactInteractionMixin,
    GameObject,
    StandingAnimationMixin,
    DamageHealthByTemperature,
    HeatInteractionMixin,
    RenderMixin,
    DeathMixin,
    ExtendedObjectMixin,
):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.noise_intensity = 0.1
        self.attractiveness = 0.1
        self.visible_size = 2.5
        self.z_level = 1.0
        self.mass = 200
        self.is_encumbrant = True
        self.num_animations_standing = 1
        self.sprite_size_x = 140
        self.sprite_size_y = 260
        # the hous3 is 3x2 with the door in the low-middle.
        # the order of the schema is important: it has to match the order of the children!!
        inner_schema = [(-1, 0, True), (1, 0, True), (-1, 1, True), (1, 1, True), (0, 1, False)]
        self.schema = {direction: inner_schema for direction in Direction}
        # Load sprites
        self.standing_sprites_locations = [
            {
                Direction.UP: [
                    f"assets/sprites/houses/house_lower.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.DOWN: [
                    f"assets/sprites/houses/house_lower.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.LEFT: [
                    f"assets/sprites/houses/house_lower.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.RIGHT: [
                    f"assets/sprites/houses/house_lower.png"
                    for i in range(self.num_animations_standing)
                ],
            }
        ]
        self.__post_init__()  # do not forget


@registry.register
class HouseOnePartOne(
    ContactInteractionMixin,
    GameObject,
    StandingAnimationMixin,
    DamageHealthByTemperature,
    HeatInteractionMixin,
    RenderMixin,
    ParentDeathIDie,
):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.noise_intensity = 0.1
        self.attractiveness = 1.1
        self.visible_size = 2.5
        self.z_level = 15.0
        self.mass = 200
        self.is_encumbrant = True
        self.num_animations_standing = 1
        self.sprite_size_x = 140 - 128
        self.sprite_size_y = 260
        self.standing_sprites_locations = [
            {
                Direction.UP: [
                    f"assets/sprites/houses/house_upper.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.DOWN: [
                    f"assets/sprites/houses/house_upper.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.LEFT: [
                    f"assets/sprites/houses/house_upper.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.RIGHT: [
                    f"assets/sprites/houses/house_upper.png"
                    for i in range(self.num_animations_standing)
                ],
            }
        ]
        self.__post_init__()  # do not forget


@registry.register
class HouseOnePartTwo(
    ContactInteractionMixin,
    GameObject,
    DamageHealthByTemperature,
    HeatInteractionMixin,
    ParentDeathIDie,
):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.noise_intensity = 0.1
        self.attractiveness = 1.1
        self.visible_size = 2.5
        self.z_level = 1.0
        self.mass = 200
        self.is_encumbrant = True
        self.__post_init__()  # do not forget


@registry.register
class Door(
    GameObject,
    ParentDeathIDie,
):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.friction_coefficient = 1
        self.noise_intensity = 0.8
        self.attractiveness = 1.1
        self.visible_size = 1.5
        self.z_level = 2.0
        self.mass = 4
        self.is_encumbrant = False
        self.is_grabbable = True
        self.level_key = ""
        self.exit_name = ""
        # Load sprites
        self.__post_init__()  # do not forget

    def enter_portal(self) -> None:
        pygame.event.post(
            pygame.event.Event(pygame.USEREVENT, code=(self.level_key, self.exit_name))
        )


@registry.register
class Baloon(
    GameObject,
    HealthDecreasesEvolution,
    StandingAnimationMixin,
    MovementAnimationMixin,
    RenderMixin,
    DeathMixin,
):
    def __init__(self, x: int, y: int, name: str, health: float, speech: str, **kwargs: Any):
        super().__init__(x, y, name, health)
        self.speech = speech
        self.z_level = 100.0
        self.actions_per_second = 3
        self.location_as_parent = True
        self.num_animations_standing = 1
        self.num_animations = 1
        self.sprite_size_y = 128
        # Load sprites
        self.__post_init__()  # do not forget

    def create_movement_sprites(self) -> None:
        self.movement_sprites = {
            Direction.UP: [self.make_balloon_surface()],
            Direction.DOWN: [self.make_balloon_surface()],
            Direction.LEFT: [self.make_balloon_surface()],
            Direction.RIGHT: [self.make_balloon_surface()],
        }

    def create_standing_sprites(self) -> None:
        self.standing_sprites = [
            {
                Direction.UP: [self.make_balloon_surface()],
                Direction.DOWN: [self.make_balloon_surface()],
                Direction.LEFT: [self.make_balloon_surface()],
                Direction.RIGHT: [self.make_balloon_surface()],
            }
        ]

    def make_balloon_surface(self) -> pygame.Surface:
        font = pygame.font.SysFont(None, 18)
        padding = 10
        line_spacing = 4  # Space between lines

        # Split text into lines
        lines = self.speech.split("\n")

        # Render each line and measure size
        rendered_lines = [font.render(line, True, BLACK) for line in lines]
        max_width = max(line.get_width() for line in rendered_lines)
        total_height = sum(line.get_height() for line in rendered_lines) + line_spacing * (
            len(lines) - 1
        )

        # Create surface with proper size
        balloon_width = max_width + 2 * padding
        balloon_height = total_height + 2 * padding
        balloon_surface = pygame.Surface((balloon_width, balloon_height), pygame.SRCALPHA)

        # Draw the rounded rectangle (the balloon)
        pygame.draw.rect(balloon_surface, WHITE, balloon_surface.get_rect(), border_radius=15)

        # Blit lines onto the surface
        y_offset = padding
        for line_surface in rendered_lines:
            balloon_surface.blit(line_surface, (padding, y_offset))
            y_offset += line_surface.get_height() + line_spacing
        self.sprite_size_y = 100 + balloon_surface.get_height()

        return balloon_surface


@registry.register
class ChestGrandpa(
    GameObject,
    StandingAnimationMixin,
    RenderMixin,
):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any) -> None:
        super().__init__(x, y, name, health)
        self.is_grabbable = True
        self.closed = True
        self.z_level = 2.0
        self.num_animations_standing = 1
        self.sprite_size_y = 32
        self.sprite_size_x = 32
        self.standing_sprites_locations = [
            {
                Direction.UP: [
                    f"assets/sprites/chest/chest_close.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.DOWN: [
                    f"assets/sprites/chest/chest_close.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.LEFT: [
                    f"assets/sprites/chest/chest_close.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.RIGHT: [
                    f"assets/sprites/chest/chest_close.png"
                    for i in range(self.num_animations_standing)
                ],
            },
            {
                Direction.UP: [
                    f"assets/sprites/chest/chest_open.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.DOWN: [
                    f"assets/sprites/chest/chest_open.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.LEFT: [
                    f"assets/sprites/chest/chest_open.png"
                    for i in range(self.num_animations_standing)
                ],
                Direction.RIGHT: [
                    f"assets/sprites/chest/chest_open.png"
                    for i in range(self.num_animations_standing)
                ],
            },
        ]
        self.__post_init__()  # do not forget

    def trigger_event(self, game) -> None:
        """
        This event consists in creating a baloon and spawning items on the floor in the exact position of the self.
        """
        if self.closed:
            self.closed = False
            baloon = registry.create(
                cls_name="Baloon",
                x=self.x,
                y=self.y,
                name="baloon",
                health=100,
                speech="Grandpa wrote a short note, saying that he closed the way north to avoid spreading\nthe frogs invasion: he would like me to go there and remove those pests.\nHe also mentioned to wear these magical robe to be able to move the rock.",
            )
            game.current_level.register(baloon)
            robe = registry.create(
                cls_name="RobeTorso",
                x=self.x,
                y=self.y,  # NOTE: maybe put + 1 here
                name="granda's robe",
                health=10,
            )
            game.current_level.register(robe)
            # make chest open
            self.current_standing_idx = 1


@registry.register
class CowMonitor(
    GameObject,
    AllChildrenDeadMixin,
):
    def __init__(self, x: int, y: int, name: str, health: float, **kwargs: Any) -> None:
        super().__init__(x, y, name, health)

    def trigger_event(self, game) -> None:
        """
        This event consists in creating a baloon and spawning items on the floor in the exact position of the self.
        """
        baloon = registry.create(
            cls_name="Baloon",
            x=self.x,
            y=self.y,
            name="baloon",
            health=10,
            speech="Noooooooo!! You killed the cow!!!",
        )
        game.current_level.register(baloon)
        game.current_level.unregister(self)
