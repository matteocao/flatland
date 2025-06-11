import pickle
import socket
import threading

from flatland.logger import Logger
from flatland.objects.items import Player  # your Player class
from flatland.objects.items_registry import registry
from flatland.world.level import Level


class GameServer:
    def __init__(self, world):
        self.world = world
        self.current_level = self.world["level_0"]
        self.current_level.get_ground_objs(self)
        self.clients = dict()  # client_id -> (socket, Player)
        self.lock = threading.Lock()
        self.logger = Logger()

    def handle_client(self, conn, addr, client_id):
        self.logger.info(f"Client {addr} connected as {client_id}")

        # Spawn player for client
        player = registry.create(
            cls_name="Player",
            x=5,
            y=5,
            name="Matte",
            health=10,
            vision_range=5,
            hearing_range=5,
            temperature=36.3,
        )  # Player(x=5, y=5, name=f"Player{client_id}", health=100, vision_range=5, hearing_range=5)
        self.current_level.register(player)
        self.clients[client_id] = (conn, player)

        try:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                keys = pickle.loads(data)  # TODO
                player.get_pressed_keys(keys)
        except:
            pass
        finally:
            self.disconnect(client_id)

    def disconnect(self, client_id):
        self.logger.info(f"Disconnecting client {client_id}")
        conn, player = self.clients.pop(client_id, (None, None))
        if conn:
            conn.close()
        if player:
            self.current_level.unregister(player)

    def update_world(self):
        # Run game logic
        self.current_level.reset_is_walkable()
        self.current_level.prepare(self.current_level._observers, self)
        self.current_level.update(None)
        self.current_level.correct_periodic_positions()

        # Broadcast state to all clients
        state = pickle.dumps(self.current_level.get_serializable_state())
        for client_id, (conn, _) in self.clients.items():
            try:
                conn.sendall(state)
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
            with self.lock:
                self.update_world()
            time.sleep(0.1)
