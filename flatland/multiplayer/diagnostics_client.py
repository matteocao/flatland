# persistent_client.py
import argparse
import socket
import time


def main():
    parser = argparse.ArgumentParser(description="Persistent diagnostic client.")
    parser.add_argument(
        "--host", type=str, required=True, help="Server IP or hostname to connect to"
    )
    parser.add_argument("--port", type=int, default=50007, help="Port number (default: 50007)")
    parser.add_argument(
        "--interval", type=float, default=1.0, help="Interval between pings (seconds)"
    )

    args = parser.parse_args()

    HOST = args.host
    PORT = args.port

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"Connecting to {HOST}:{PORT} ...")
            s.connect((HOST, PORT))
            print("Connected to server.")

            while True:
                message = b"PING"
                s.sendall(message)
                print("Sent:", message)
                data = s.recv(1024)
                print("Received:", data.decode())
                time.sleep(args.interval)
    except Exception as e:
        print(f"Connection failed: {e}")


if __name__ == "__main__":
    main()
