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
    # TODO: this will create one instance per object, but this is not general
    for cls_name in registry._registry:
        if cls_name != "Ground":
            rnd_name = "".join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(6)
            )
            obj = registry.create(
                cls_name=cls_name,
                x=random.randint(0, 9),
                y=random.randint(0, 9),
                name=rnd_name,
                health=random.randint(3, 9),
                vision_range=5,
                hearing_range=3,
                temperature=12.3,
            )
            world.register(obj)


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
