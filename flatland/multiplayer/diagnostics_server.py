"""diagnostic script, not used for the game"""

import socket

HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 50007  # Use any test port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                print("Connection closed by client")
                break
            print(f"Received: {data.decode()}")
            conn.sendall(b"ACK: " + data)
