import socket
import argparse
import threading
import sys
import hashlib
import time
import logging


class P2PTracker:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = {} # Dictionary to keep track of clients and their file chunks
        self.lock = threading.Lock() # For thread-safe operations on clients dictionary
    
    def start_server(self):
        """Starts the tracker server."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Tracker running on {self.host}:{self.port}")
        while True:
            client_socket, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()
    
    def handle_client(self, client_socket, addr):
        """Handles communication with a connected client."""
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                # Process the data from client
                # This can include registering a new client, updating available file chunks, etc.
            except:
                break
        client_socket.close()
        # Remove client from clients dictionary
        with self.lock:
            if addr in self.clients:
                del self.clients[addr]
    
    # Add methods for managing file chunks among clients
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="P2P Tracker")
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host address of the tracker')
    parser.add_argument('--port', type=int, default=8000, help='Port on which the tracker will run')
    args = parser.parse_args()
    
    tracker = P2PTracker(args.host, args.port)
    tracker.start_server()
