import glob
import random
import string
from typing import TYPE_CHECKING

from ..consts import MAX_X, MAX_Y, TILE_SIZE
from ..objects.items_registry import registry
from .build_tile_map import build_tile_map
from .world import world

if TYPE_CHECKING:
    from ..objects.items import Ground


# Register objects
def register_objects() -> None:

    cow = registry.create(
        cls_name="Cow",
        x=random.randint(0, 9),
        y=random.randint(0, 9),
        name="lola",
        health=5,
        vision_range=5,
        hearing_range=3,
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
        x=player.x,
        y=player.y,
        name="robe",
        health=100,
    )
    robe_torso.parent = player
    robe_torso.actions_per_second = player.actions_per_second
    player.children.append(robe_torso)
    cow_shadow.parent = cow
    cow.children.append(cow_shadow)

    world.register(cow)
    world.register(cow_shadow)
    world.register(player)
    world.register(stone)
    world.register(robe_torso)


# register terrain
def register_terrain() -> None:
    cls_name = "Ground"
    list_of_possible_tiles: list["Ground"] = []
    png_files = glob.glob("assets/sprites/terrain/*.png")
    for tile_name_png in png_files:
        tile_name = tile_name_png[:-4]

        obj: "Ground" = registry.create(  # type: ignore
            cls_name=cls_name, x=0, y=0, name=tile_name, health=10, tile_name=tile_name
        )
        list_of_possible_tiles.append(obj)
    terrain = build_tile_map(list_of_possible_tiles)
    for i, lst_obj in enumerate(terrain):
        for j, obj in enumerate(lst_obj):
            new_obj = obj.clone()
            new_obj.y = i
            new_obj.x = j
            world.register(new_obj)
