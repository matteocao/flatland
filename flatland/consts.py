"""
This file contains the main game constans
"""

from dataclasses import dataclass
from enum import Enum

TILE_SIZE = 64
MAX_X = 800 // TILE_SIZE
MAX_Y = 600 // TILE_SIZE


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


BLACK = (0, 0, 0)

WHITE = (255, 255, 255)
