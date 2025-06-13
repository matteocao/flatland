# diagnostic_client_argparse.py
import argparse
import socket


def main():
    parser = argparse.ArgumentParser(description="Diagnostic client to test socket connection.")
    parser.add_argument(
        "--host", type=str, required=True, help="Server IP or hostname to connect to"
    )
    parser.add_argument("--port", type=int, default=50007, help="Port number (default: 50007)")

    args = parser.parse_args()

    HOST = args.host
    PORT = args.port

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"Connecting to {HOST}:{PORT} ...")
            s.connect((HOST, PORT))
            print("Connected to server.")
            s.sendall(b"Hello Server!")
            data = s.recv(1024)
            print(f"Received from server: {data.decode()}")
    except Exception as e:
        print(f"Connection failed: {e}")


if __name__ == "__main__":
    main()
