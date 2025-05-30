from dataclasses import dataclass

TILE_SIZE = 32
MAX_X = 800 // TILE_SIZE
MAX_Y = 600 // TILE_SIZE


@dataclass
class Direction:
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
