import pygame

from .world.world import GameWorld


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("AI-Driven 2D RPG")
    clock = pygame.time.Clock()

    world = GameWorld(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        world.handle_input(keys)
        world.update()
        world.render()
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
