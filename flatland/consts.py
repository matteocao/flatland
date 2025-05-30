from dataclasses import dataclass
from enum import Enum

TILE_SIZE = 32
MAX_X = 800 // TILE_SIZE
MAX_Y = 600 // TILE_SIZE


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
