import pygame

from .consts import MAX_X, MAX_Y, TILE_SIZE
from .game import Game
from .world.world import world

if __name__ == "__main__":
    screen = pygame.display.set_mode((MAX_X * TILE_SIZE, MAX_Y * TILE_SIZE))
    game = Game(world, screen)
    game.main()
