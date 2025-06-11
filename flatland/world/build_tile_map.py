import random
from typing import TYPE_CHECKING

from ..consts import MAX_X, MAX_Y

if TYPE_CHECKING:
    from ..objects.items import Ground


def build_tile_map(tile_objects: list["Ground"], width: int, height: int) -> list[list["Ground"]]:
    """
    Dynamically build a tile map by glueing together only tiles with mathcing interafaces
    """
    # tile_objects: list of Ground instances, each with .tile_name and .nswe_neigh
    tile_map: list[list["Ground"]] = [[None for _ in range(width)] for _ in range(height)]  # type: ignore

    for i in range(height):
        for j in range(width):
            candidates: list["Ground"] = []

            for tile in tile_objects:
                n, s, w, e = tile.nswe_neigh

                # Check compatibility with tile above (north)
                if i > 0:
                    above_tile = tile_map[i - 1][j]
                    if above_tile is None or above_tile.nswe_neigh[1] != n:
                        continue

                # Check compatibility with tile to the left (west)
                if j > 0:
                    left_tile = tile_map[i][j - 1]
                    if left_tile is None or left_tile.nswe_neigh[3] != w:
                        continue

                candidates.append(tile)

            if not candidates:
                raise RuntimeError(f"No compatible tile found for position ({i},{j})")

            tile_map[i][j] = random.choice(candidates)

    return tile_map
