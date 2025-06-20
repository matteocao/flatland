"""
This is the server entry point
"""

import pygame

from flatland.multiplayer.server import GameServer
from flatland.world.world import world

if __name__ == "__main__":
    GameServer(world).run()
