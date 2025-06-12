import pickle
import socket
import struct
import threading
from typing import Any

import pygame

from flatland.logger import Logger
from flatland.objects.items import Player  # your Player class
from flatland.objects.items_registry import registry
from flatland.world.level import Level


class GameServer:
    def __init__(self, world: dict[str, Level]) -> None:
        self.world = world
        for level in self.world.values():
            self.current_level = level
            level.get_ground_objs(self)  # type: ignore
        del self.current_level
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
        del self.current_level

        with self.lock:
            self.clients[client_id] = (conn, player)

            # 👇 Send full world state immediately
            world_state = self.client_levels[client_id].get_serializable_state()
            full_state = pickle.dumps(world_state)
            length_prefix = struct.pack("!I", len(full_state))
            conn.sendall(length_prefix + full_state)

        try:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                keys = pickle.loads(data)
                player.get_pressed_keys(keys)  # type: ignore
        except:
            pass
        finally:
            self.disconnect(client_id)

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
                level.reset_is_walkable()
                level.prepare(level._observers, self)
                level.update(None)
                level.correct_periodic_positions()

            # Broadcast state to all clients
            for client_id, (conn, _) in self.clients.items():
                state = pickle.dumps(self.client_levels[client_id].get_serializable_state())
                length_prefix = struct.pack("!I", len(state))  # 4-byte length prefix
                try:
                    conn.sendall(length_prefix + state)
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
        import time

        while True:
            self.update_world()
            time.sleep(0.1)
