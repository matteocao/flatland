import warnings

import pygame

from .consts import MAX_X, MAX_Y
from .world.world import world

# initialise pygame
pygame.init()
pygame.display.set_mode((1, 1))  # Minimal dummy window
try:
    pygame.mixer.init()
except pygame.error as e:
    # fallback: disable sound if mixer init fails (e.g., in CI)
    warnings.warn(f"Could not load mixer, {e}")


def main():

    screen = pygame.display.set_mode((MAX_X, MAX_Y))
    pygame.display.set_caption("AI-Driven 2D RPG")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))

        keys = pygame.key.get_pressed()
        # send keys to the user
        world.send_keys_to_user(keys)
        near_objs = world._observers
        world.prepare(near_objs)
        world.update(keys)
        world.render(screen)
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
