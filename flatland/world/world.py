import pygame
from ..registry import registry
from ..objects.objects import Player, Stone, Animal, NPC
from ..moderator import InteractionModerator
from ..tilemap import TileMap

class GameWorld:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.objects = []
        self.width = screen.get_width() // 32
        self.height = screen.get_height() // 32
        self.interactions = InteractionModerator()
        self.tilemap = TileMap(self.width, self.height)

        self.player = Player(x=5, y=5)
        self.objects.append(self.player)
        self.objects.append(Stone(x=6, y=5))
        self.objects.append(Animal(x=4, y=5))
        self.objects.append(NPC(x=5, y=6))

    def handle_input(self, keys):
        self.player.handle_input(keys, self.width, self.height, self.objects)

    def update(self):
        for obj in self.objects:
            obj.update(self)
        self.interactions.resolve(self.objects, self)

    def render(self):
        self.screen.fill((0, 0, 0))
        for obj in self.objects:
            obj.render(self.screen)