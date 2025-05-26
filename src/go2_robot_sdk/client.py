#!/usr/bin/env python3
# distance_tcp.py

import socket

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 8000      # Port to listen on

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"Listening for distance data on {HOST}:{PORT}...")

        # 무한 루프: 클라이언트가 연결될 때마다 처리
        while True:
            conn, addr = server.accept()
            print(f"Client connected from {addr}")
            with conn:
                try:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            # 클라이언트가 연결을 끊으면 내부 루프 탈출
                            break
                        msg = data.decode('utf-8').strip()
                        print(f"Received distance: {msg} m")
                except Exception as e:
                    print(f"Connection error: {e}")
                finally:
                    print("Client disconnected.")

if __name__ == '__main__':
    main()
