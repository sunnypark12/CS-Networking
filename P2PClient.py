import socket
import argparse
import threading
import sys
import hashlib
import time
import logging
import os

class P2PClient:
    def __init__(self, server_host, server_port, folder_path):
        self.server_host = server_host
        self.server_port = server_port
        self.folder_path = folder_path
        self.server_socket = None
        self.chunk_info = {} # Stores chunk index and file names
        self.load_local_chunks()

    def connect_to_tracker(self):
        """Connects to the P2PTracker."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((self.server_host, self.server_port))
        # Send local chunk information to tracker
        for chunk, _ in self.chunk_info.items():
            msg = f"LOCAL_CHUNKS{chunk}{socket.gethostname()}{self.server_socket.getsockname()[1]}"
            self.server_socket.sendall(msg.encode())

    def load_local_chunks(self):
        """Loads local chunk information from local_chunks.txt."""
        try:
            with open(os.path.join(self.folder_path, 'local_chunks.txt'), 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        self.chunk_info[parts[0]] = parts[1]
        except FileNotFoundError:
            print("local_chunks.txt not found in the specified folder.")
            sys.exit(1)

    # Method to request missing chunks from tracker and download them from peers
    # Method to handle incoming requests from other peers (if implementing server functionality within client)
    # Additional methods as per the assignment requirements

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="P2P Client")
    parser.add_argument('folder_path', type=str, help='The path to the folder containing local_chunks.txt')
    parser.add_argument('--server_host', default='localhost', type=str, help='The host address of the P2PTracker')
    parser.add_argument('--server_port', default=5100, type=int, help='The port number of the P2PTracker')
    args = parser.parse_args()

    client = P2PClient(args.server_host, args.server_port, args.folder_path)
    client.connect_to_tracker()
    # client.start() or any other methods to begin its operations
