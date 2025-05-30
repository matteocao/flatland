import pygame

from .consts import MAX_X, MAX_Y
from .world.world import world


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
