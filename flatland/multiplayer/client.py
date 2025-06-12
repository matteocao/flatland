import copy
import pickle
import socket
import struct
from typing import TYPE_CHECKING, Any

import pygame

from flatland.consts import MAX_X, MAX_Y, TILE_SIZE
from flatland.objects.items_registry import registry
from flatland.world.level import Level

if TYPE_CHECKING:
    from flatland.objects.base_objects import GameObject


class GameClient:
    def __init__(self, host: str, port: int) -> None:
        self.level = Level()
        self.obj_map: dict[str, "GameObject"] = {}  # key = object ID or unique hash
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.init_world_state()
        pygame.init()
        self.screen = pygame.display.set_mode((MAX_X * TILE_SIZE, MAX_Y * TILE_SIZE))
        self.clock = pygame.time.Clock()
        self.old_world_state: Any = None

    def init_world_state(self):
        # Receive full initial world state
        length_data = self.recv_all(self.sock, 4)
        message_length = struct.unpack("!I", length_data)[0]
        data = self.recv_all(self.sock, message_length)
        payload = pickle.loads(data)

        world_state = payload["world_state"]
        self.my_player_id = payload["player_id"]  # 👈 Save your player ID

        for obj_data in world_state["objects"]:
            obj_id = obj_data["id"]
            instance = registry.create(
                cls_name=obj_data["cls_name"],
                x=obj_data["x"],
                y=obj_data["y"],
                name=obj_data["name"],
                health=obj_data["health"],
                vision_range=5,
                hearing_range=5,
                temperature=36.3,
                tile_name=obj_data["tile_name"],
            )
            for k, v in obj_data.items():
                if k != "cls_name":
                    setattr(instance, k, v)
            self.level.register(instance)
            self.obj_map[obj_id] = instance

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

    def request_portal(self, target_level_key: str) -> None:
        message = {"type": "portal_request", "target_level": target_level_key}
        self.sock.sendall(pickle.dumps(message))

    def run(self) -> None:
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
            portals: list[dict[str, Any]] = []
            players: list[dict[str, Any]] = []
            for obj in world_state["objects"]:
                if obj["cls_name"] == "Portal":
                    portals.append(obj)
                if obj["cls_name"] == "Player":
                    players.append(obj)
            self.render(world_state)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # check for the portal request to enter
            for portal in portals:
                player = [player for player in players if player["id"] == self.my_player_id][0]
                if keys[pygame.K_q] and player["x"] == portal["x"] and player["y"] == portal["y"]:
                    self.request_portal(portal["level_key"])
                    break

            pygame.display.flip()
            self.clock.tick(10)

    def render(self, world_state: dict[str, list[dict[str, Any]]]) -> None:
        self.screen.fill((0, 0, 0))

        # Build set of current object IDs received from server
        incoming_ids = set()

        for obj_data in world_state["objects"]:
            obj_id = obj_data["id"]  # <-- unique ID of object
            incoming_ids.add(obj_id)

            if obj_id in self.obj_map:
                # Object already exists → update fields
                instance = self.obj_map[obj_id]
                for k, v in obj_data.items():
                    if k != "cls_name":
                        setattr(instance, k, v)
            else:
                # New object → create it
                instance = registry.create(
                    cls_name=obj_data["cls_name"],
                    x=obj_data["x"],
                    y=obj_data["y"],
                    name=obj_data["name"],
                    health=obj_data["health"],
                    vision_range=5,
                    hearing_range=5,
                    temperature=36.3,
                    tile_name=obj_data["tile_name"],
                )
                for k, v in obj_data.items():
                    if k != "cls_name":
                        setattr(instance, k, v)
                self.level.register(instance)
                self.obj_map[obj_id] = instance

        # Unregister missing objects
        existing_ids = set(self.obj_map.keys())
        removed_ids = existing_ids - incoming_ids
        for obj_id in removed_ids:
            inst = self.obj_map.pop(obj_id)
            self.level.unregister(inst)

        # Render everything
        self.level.render(self.screen)
