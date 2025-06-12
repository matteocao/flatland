import argparse

from flatland.multiplayer.client import GameClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Flatland Game Client")
    parser.add_argument("--ip", type=str, default="0.0.0.0", help="Server IP address")
    parser.add_argument("--port", type=int, default=12345, help="Server port")

    args = parser.parse_args()

    GameClient(args.ip, args.port).run()
