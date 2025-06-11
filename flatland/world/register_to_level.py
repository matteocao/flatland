import glob
import random
import string
from typing import TYPE_CHECKING

from ..consts import MAX_X, MAX_Y, TILE_SIZE
from ..objects.items_registry import registry
from .build_tile_map import build_tile_map
from .level import Level

if TYPE_CHECKING:
    from ..objects.items import Ground


# Register objects
def register_objects(level: Level) -> Level:

    cow = registry.create(
        cls_name="Cow",
        x=random.randint(0, 9),
        y=random.randint(0, 9),
        name="lola",
        health=5,
        vision_range=5,
        hearing_range=3,
    )
    goblin = registry.create(
        cls_name="Goblin",
        x=random.randint(0, 9),
        y=random.randint(0, 9),
        name="ashpack",
        health=9,
        vision_range=3,
        hearing_range=5,
    )
    stone = registry.create(
        cls_name="Stone",
        x=random.randint(0, 9),
        y=random.randint(0, 9),
        name="a rock",
        health=50,
    )
    cow_shadow = registry.create(
        cls_name="CowShadow",
        x=cow.x,
        y=cow.y,
        name="lola_shadow",
        health=100,
    )
    player = registry.create(
        cls_name="Player",
        x=random.randint(0, 9),
        y=random.randint(0, 9),
        name="Matte",
        health=10,
        vision_range=5,
        hearing_range=5,
        temperature=36.3,
    )
    robe_torso = registry.create(
        cls_name="RobeTorso",
        x=random.randint(0, 9),
        y=random.randint(0, 9),
        name="robe",
        health=100,
    )
    shoes = registry.create(
        cls_name="Shoes",
        x=random.randint(0, 9),
        y=random.randint(0, 9),
        name="shoes",
        health=100,
    )
    hood = registry.create(
        cls_name="Hood",
        x=random.randint(0, 9),
        y=random.randint(0, 9),
        name="hood",
        health=100,
    )
    skirt = registry.create(
        cls_name="Skirt",
        x=random.randint(0, 9),
        y=random.randint(0, 9),
        name="skirt",
        health=100,
    )
    orangetree = registry.create(
        cls_name="OrangeTreeOne",
        x=random.randint(0, 9),
        y=random.randint(0, 9),
        name="orangetree",
        health=200,
    )

    cow_shadow.parent = cow
    cow.children.append(cow_shadow)

    level.register(cow)
    level.register(cow_shadow)

    level.register(stone)
    level.register(goblin)

    # player stuff
    level.register(player)
    level.register(robe_torso)
    level.register(shoes)
    level.register(hood)
    level.register(skirt)
    level.register(orangetree)
    return level


# register terrain
def register_terrain(level: Level, width: int, height: int) -> Level:
    cls_name = "Ground"
    list_of_possible_tiles: list["Ground"] = []
    png_files = glob.glob("assets/sprites/terrain/*.png")
    for tile_name_png in png_files:
        tile_name = tile_name_png[:-4]

        obj: "Ground" = registry.create(  # type: ignore
            cls_name=cls_name, x=0, y=0, name=tile_name, health=10, tile_name=tile_name
        )
        list_of_possible_tiles.append(obj)
    terrain = build_tile_map(list_of_possible_tiles, width, height)
    for i, lst_obj in enumerate(terrain):
        for j, obj in enumerate(lst_obj):
            new_obj: "Ground" = registry.create(  # type: ignore
                cls_name=cls_name,
                x=j,
                y=i,
                name=obj.tile_name,
                health=obj.health,
                tile_name=obj.tile_name,
            )
            level.register(new_obj)
    return level
