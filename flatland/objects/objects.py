import pygame
import random
from abc import ABC, abstractmethod
from ..registry import registry

TILE_SIZE = 32

class GameObject(ABC):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @abstractmethod
    def update(self, world):
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface):
        pass

    def interact(self, other, world):
        pass

@registry.auto_register("characters")
class Player(GameObject):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.color = (0, 255, 0)

    def handle_input(self, keys, max_x, max_y, objects):
        dx = dy = 0
        if keys[pygame.K_UP]: dy = -1
        elif keys[pygame.K_DOWN]: dy = 1
        elif keys[pygame.K_LEFT]: dx = -1
        elif keys[pygame.K_RIGHT]: dx = 1

        new_x = (self.x + dx) % max_x
        new_y = (self.y + dy) % max_y

        blocked = False
        for obj in objects:
            if obj.x == new_x and obj.y == new_y:
                if isinstance(obj, Stone):
                    obj.x = (obj.x + dx) % max_x
                    obj.y = (obj.y + dy) % max_y
                    obj.moving = True
                else:
                    blocked = True

        if not blocked:
            self.x = new_x
            self.y = new_y

    def update(self, world):
        pass

    def render(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(
            self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE
        ))

    def interact(self, other, world):
        print(f"Player interacts with {type(other).__name__}")

@registry.auto_register("inanimate")
class Stone(GameObject):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.color = (128, 128, 128)
        self.moving = False

    def update(self, world):
        pass

    def render(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(
            self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE
        ))

@registry.auto_register("animals")
class Animal(GameObject):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.color = (255, 255, 0)
        self.vision_range = 3
        self.health = 3

    def update(self, world):
        if self.health <= 0:
            world.objects.remove(self)
            return

        player = self._see_player(world)
        if player:
            dx = player.x - self.x
            dy = player.y - self.y
            if abs(dx) > abs(dy):
                self.x += 1 if dx > 0 else -1
            else:
                self.y += 1 if dy > 0 else -1
        else:
            self._random_move(world)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(
            self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE
        ))

    def _see_player(self, world):
        for obj in world.objects:
            if isinstance(obj, Player):
                if abs(obj.x - self.x) <= self.vision_range and abs(obj.y - self.y) <= self.vision_range:
                    return obj
        return None

    def _random_move(self, world):
        direction = random.choice([(1,0), (-1,0), (0,1), (0,-1), (0,0)])
        self.x = (self.x + direction[0]) % world.width
        self.y = (self.y + direction[1]) % world.height

    def interact(self, other, world):
        print(f"Animal interacts with {type(other).__name__}")

@registry.auto_register("npcs")
class NPC(GameObject):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.color = (0, 0, 255)

    def update(self, world):
        if random.random() < 0.1:
            self.x = (self.x + random.choice([-1, 0, 1])) % world.width
            self.y = (self.y + random.choice([-1, 0, 1])) % world.height

    def render(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(
            self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE
        ))

    def interact(self, other, world):
        print(f"NPC interacts with {type(other).__name__}")