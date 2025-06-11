import pickle
import socket

import pygame

from flatland.consts import MAX_X, MAX_Y, TILE_SIZE


class GameClient:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        pygame.init()
        self.screen = pygame.display.set_mode((MAX_X * TILE_SIZE, MAX_Y * TILE_SIZE))
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            keys = pygame.key.get_pressed()
            pygame.event.pump()
            keys_serialized = self.serialize_keys(keys)
            self.sock.sendall(pickle.dumps(keys_serialized))

            data = self.sock.recv(65536)
            world_state = pickle.loads(data)  # TODO
            self.render(world_state)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()
            self.clock.tick(10)

    def serialize_keys(self, keys):
        return [i for i, pressed in enumerate(keys) if pressed]

    def render(self, world_state):  # TODO
        self.screen.fill((0, 0, 0))
        for obj in world_state["objects"]:
            x, y = obj["x"], obj["y"]
            pygame.draw.rect(self.screen, (255, 0, 0), (x * 32, y * 32, 32, 32))
