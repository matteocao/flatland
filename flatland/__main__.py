import warnings

import pygame

from .consts import MAX_X, MAX_Y, TILE_SIZE
from .logger import Logger
from .objects import items
from .world.register_to_world import register_objects, register_terrain
from .world.world import world

# initialise pygame for CI tests
pygame.init()
pygame.display.set_mode((1, 1))  # Minimal dummy window
try:
    pygame.mixer.init()
except pygame.error as e:
    # fallback: disable sound if mixer init fails (e.g., in CI)
    warnings.warn(f"Could not load mixer, {e}")


def main():

    screen = pygame.display.set_mode((MAX_X * TILE_SIZE, MAX_Y * TILE_SIZE))
    pygame.display.set_caption("Flatland")
    clock = pygame.time.Clock()
    logger = Logger()
    register_terrain()
    register_objects()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))  # to cancel previous state

        keys = pygame.key.get_pressed()

        # send keys to the user
        world.send_keys_to_user(keys)
        near_objs = world._observers
        # logger.info(near_objs)
        world.prepare(near_objs)
        world.update(keys)
        world.correct_periodic_positions()  # this is needed now that the world is periodic
        world.render(screen)
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
