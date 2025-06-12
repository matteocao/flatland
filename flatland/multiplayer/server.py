import pickle
import socket
import struct
import threading
import time
from typing import Any

import pygame

from flatland.logger import Logger
from flatland.objects.items import Player  # your Player class
from flatland.objects.items_registry import registry
from flatland.world.level import Level


class GameServer:
    def __init__(self, world: dict[str, Level]) -> None:
        self.world = world
        self.current_level: Any = None
        for level in self.world.values():
            self.current_level = level
            level.get_ground_objs(self)  # type: ignore
        self.current_level = None
        self.clients: dict[int, tuple] = dict()  # client_id -> (socket, Player)
        self.lock = threading.Lock()
        self.logger = Logger()
        self.client_levels: dict[int, Level] = dict()  # the key is the client_id

    def handle_client(self, conn: Any, addr: Any, client_id: int):
        self.logger.info(f"Client {addr} connected as {client_id}")

        # Create player for client
        player = registry.create(
            cls_name="Player",
            x=5,
            y=5,
            name=f"Player{client_id}",
            health=10,
            vision_range=5,
            hearing_range=5,
            temperature=36.3,
        )
        self.client_levels[client_id] = self.world["level_0"]
        self.client_levels[client_id].register(player)
        self.current_level = self.client_levels[client_id]
        self.client_levels[client_id].get_ground_objs(self)  # type: ignore
        self.current_level = None

        with self.lock:
            self.clients[client_id] = (conn, player)

            # 👇 Send full world state immediately
            world_state = self.client_levels[client_id].get_serializable_state()
            payload = {
                "world_state": world_state,
                "player_id": player.id,  # 👈 send player id to client
                "level_key": self.client_levels[client_id].level_key,
            }
            full_state = pickle.dumps(payload)
            length_prefix = struct.pack("!I", len(full_state))
            conn.sendall(length_prefix + full_state)

        try:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                keys = pickle.loads(data)
                if isinstance(keys, dict) and keys.get("type") == "portal_request":
                    self.process_portal(client_id, keys["target_level"])
                else:
                    player.get_pressed_keys(keys)  # type: ignore
        except:
            pass
        finally:
            self.disconnect(client_id)

    def process_portal(self, client_id: int, target_level_key: str):
        self.logger.info(f"Processing portal request for client {client_id} -> {target_level_key}")

        with self.lock:
            player = self.clients[client_id][1]
            old_level = self.client_levels[client_id]

            # Unregister player from old level
            old_level.unregister(player)
            for obj in player.children:
                old_level.unregister(obj)

            # Move player to new level
            new_level = self.world[target_level_key]

            # Move player to portal spawn point
            portal = next(obj for obj in new_level._observers if obj.__class__.__name__ == "Portal")
            player.x = portal.x
            player.y = portal.y

            # Register player in new level
            for obj in player.children:
                new_level.register(obj)
            new_level.register(player)

            self.current_level = new_level
            new_level.get_ground_objs(self)  # type: ignore
            self.current_level = None
            self.client_levels[client_id] = new_level

    def disconnect(self, client_id: int):
        self.logger.info(f"Disconnecting client {client_id}")
        with self.lock:
            conn, player = self.clients.pop(client_id, (None, None))
        if conn:
            conn.close()
        if player:
            self.client_levels[client_id].unregister(player)

    def update_world(self):
        with self.lock:
            # update each level where there is at least one client
            for level in set(self.client_levels.values()):
                # Run game logic
                self.current_level = level
                level.reset_is_walkable()
                level.prepare(level._observers, self)
                level.update(None)
                level.correct_periodic_positions()
                self.current_level = None

            # Broadcast state to all clients
            for client_id, (conn, _) in self.clients.items():
                world_state = self.client_levels[client_id].get_serializable_state()
                payload = {
                    "world_state": world_state,
                    "level_key": self.client_levels[client_id].level_key,
                }
                full_state = pickle.dumps(payload)
                length_prefix = struct.pack("!I", len(full_state))  # 4-byte length prefix
                try:
                    conn.sendall(length_prefix + full_state)
                except:
                    self.disconnect(client_id)

    def run(self, host="0.0.0.0", port=12345):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen()
        print("Server listening...")

        threading.Thread(target=self.world_loop, daemon=True).start()

        client_id = 0
        while True:
            conn, addr = server_socket.accept()
            threading.Thread(
                target=self.handle_client, args=(conn, addr, client_id), daemon=True
            ).start()
            client_id += 1

    def world_loop(self):
        while True:
            self.update_world()
            time.sleep(0.1)
