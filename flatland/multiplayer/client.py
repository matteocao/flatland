import pickle
import socket
import struct

import pygame

from flatland.consts import MAX_X, MAX_Y, TILE_SIZE
from flatland.objects.items_registry import registry
from flatland.world.level import Level


class GameClient:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        pygame.init()
        self.screen = pygame.display.set_mode((MAX_X * TILE_SIZE, MAX_Y * TILE_SIZE))
        self.clock = pygame.time.Clock()

    @staticmethod
    def recv_all(sock, n):
        """Helper function to receive exactly n bytes"""
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                raise ConnectionError("Socket connection broken")
            data.extend(packet)
        return data

    def run(self):
        running = True
        while running:
            keys = pygame.key.get_pressed()
            pygame.event.pump()
            self.sock.sendall(pickle.dumps(keys))

            # First read 4 bytes (message length)
            length_data = self.recv_all(self.sock, 4)
            message_length = struct.unpack("!I", length_data)[0]

            # Then read the full message
            data = self.recv_all(self.sock, message_length)
            world_state = pickle.loads(data)
            self.render(world_state)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()
            self.clock.tick(10)

    def render(self, world_state):  # TODO
        self.screen.fill((0, 0, 0))
        level = Level()
        for obj in world_state["objects"]:
            inst = registry.create(
                cls_name=obj["cls_name"],
                x=obj["x"],
                y=obj["y"],
                name=obj["name"],
                health=obj["health"],
                vision_range=5,
                hearing_range=5,
                temperature=36.3,
                tile_name=obj["tile_name"],
            )
            for k, v in obj.items():
                if k != "cls_name":
                    setattr(inst, k, v)
            level.register(inst)
        level.render(self.screen)
