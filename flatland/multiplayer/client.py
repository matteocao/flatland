import copy
import pickle
import socket
import struct
import threading
import time
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
        self.running = True
        self.obj_map: dict[str, "GameObject"] = {}  # key = object ID or unique hash
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.init_world_state()
        pygame.init()
        self.screen = pygame.display.set_mode((MAX_X * TILE_SIZE, MAX_Y * TILE_SIZE))
        self.clock = pygame.time.Clock()
        self.old_world_state: Any = None

    def init_world_state(self) -> None:
        # Receive full initial world state
        length_data = self.recv_all(self.sock, 4)
        message_length = struct.unpack("!I", length_data)[0]
        data = self.recv_all(self.sock, message_length)
        payload = pickle.loads(data)

        world_state = payload["world_state"]
        self.my_player_id = payload["player_id"]  # 👈 Save your player ID
        self.current_level_key = payload["level_key"]

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
        # connect parents and children
        for obj in self.level._observers:
            if obj.parent_id:
                self.obj_map[obj.parent_id].children.append(obj)
                obj.parent = self.obj_map[obj.parent_id]

    @staticmethod
    def recv_all(sock, n):
        """Helper function to receive exactly n bytes"""
        data = bytearray()
        while len(data) < n:
            try:
                packet = sock.recv(n - len(data))
                if not packet:
                    raise ConnectionError(
                        f"Socket connection broken while expecting {n} bytes, got only {len(data)} bytes"
                    )
                data.extend(packet)
            except Exception as e:
                print(f"recv_all exception: {e}, received so far: {len(data)} / {n}")
                raise
        return data

    def request_portal(self, target_level_key: str, exit_name: str) -> None:
        message = {
            "type": "portal_request",
            "target_level": target_level_key,
            "exit_name": exit_name,
        }
        payload = pickle.dumps(message)
        length_prefix = struct.pack("!I", len(payload))
        self.sock.sendall(length_prefix + payload)

    def send_inputs(self) -> None:
        while self.running:
            keys = pygame.key.get_pressed()
            payload = pickle.dumps(keys)
            length_prefix = struct.pack("!I", len(payload))
            self.sock.sendall(length_prefix + payload)
            time.sleep(1 / 20)  # 60Hz input send

    def receive_world(self) -> None:
        while self.running:
            try:
                length_data = self.recv_all(self.sock, 4)
                message_length = struct.unpack("!I", length_data)[0]
                data = self.recv_all(self.sock, message_length)
                payload = pickle.loads(data)
                world_state = payload["world_state"]
                level_key = payload["level_key"]

                # Update local state (must be thread-safe)
                with self.state_lock:
                    self.latest_world_state = world_state
                    self.latest_level_key = level_key

            except Exception as e:
                print(f"Receiver thread exception: {e}")
                self.running = False

    def run(self) -> None:
        self.running = True
        self.state_lock = threading.Lock()
        self.latest_world_state = None
        self.latest_level_key = None

        threading.Thread(target=self.send_inputs, daemon=True).start()
        threading.Thread(target=self.receive_world, daemon=True).start()

        while self.running:
            pygame.event.pump()

            with self.state_lock:
                world_state = self.latest_world_state
                level_key = self.latest_level_key

            if world_state is not None:
                portals, players = [], []
                for obj in world_state["objects"]:
                    if obj["level_key"] is not None:
                        portals.append(obj)
                    if obj["cls_name"] == "Player":
                        players.append(obj)

                self.render(world_state, level_key)

                # portal request handling remains the same
                for portal in portals:
                    player = [player for player in players if player["id"] == self.my_player_id][0]
                    keys = pygame.key.get_pressed()
                    if (
                        keys[pygame.K_q]
                        and player["x"] == portal["x"]
                        and player["y"] == portal["y"]
                    ):
                        self.request_portal(portal["level_key"], portal["exit_name"])
                        break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()
            self.clock.tick(10)

    def render(self, world_state: dict[str, list[dict[str, Any]]], level_key: str) -> None:
        self.screen.fill((0, 0, 0))

        # Build set of current object IDs received from server
        incoming_ids = set()
        if self.current_level_key != level_key:
            self.level = Level(level_key)
            self.obj_map.clear()
            self.current_level_key = level_key

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
        # connect parents and children
        for obj in self.level._observers:
            obj.children.clear()
        for obj in self.level._observers:
            if obj.parent:
                obj.parent = None
            if obj.parent_id:
                try:
                    self.obj_map[obj.parent_id].children.append(obj)
                    obj.parent = self.obj_map[obj.parent_id]
                    if obj.location_as_parent:
                        obj.x = self.obj_map[obj.parent_id].x
                        obj.y = self.obj_map[obj.parent_id].y
                except KeyError:
                    pass
        # Unregister missing objects
        existing_ids = set(self.obj_map.keys())
        removed_ids = existing_ids - incoming_ids
        for obj_id in removed_ids:
            inst = self.obj_map.pop(obj_id)
            self.level.unregister(inst)

        # Render everything
        self.level.render(self.screen)
