import glob

import yaml  # type: ignore

from flatland.objects.items import Ground
from flatland.objects.items_registry import registry
from flatland.world.build_tile_map import build_tile_map


def dump_ground_tiles_to_yaml_snippet(terrain: list[list[Ground]]) -> str:
    tile_objects = []
    for y, row in enumerate(terrain):
        for x, tile in enumerate(row):
            tile_entry = {
                "cls_name": "Ground",
                "name": f"{tile.tile_name}_{x}_{y}",
                "x": x,
                "y": y,
                "health": tile.health,
                "tile_name": tile.tile_name,
            }
            tile_objects.append(tile_entry)

    return yaml.dump({"objects": tile_objects}, sort_keys=False)


if __name__ == "__main__":
    list_of_possible_tiles: list[Ground] = []
    png_files = glob.glob("assets/sprites/terrain/*.png")
    for tile_name_png in png_files:
        tile_name = tile_name_png[:-4]

        obj: "Ground" = registry.create(  # type: ignore
            cls_name="Ground", x=0, y=0, name=tile_name, health=10, tile_name=tile_name
        )
        list_of_possible_tiles.append(obj)
    terrain = build_tile_map(list_of_possible_tiles, width=12, height=9)
    print(dump_ground_tiles_to_yaml_snippet(terrain))
