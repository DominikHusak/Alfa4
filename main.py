import json
import socket
import threading
import time

from conf import *

class UDPListener(threading.Thread):
    def __init__(self, sock, callback):
        super().__init__()
        self.sock = sock
        self.callback = callback
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            data, addr = self.sock.recvfrom(1024)
            message = json.loads(data.decode())
            self.callback(message, addr)

    def stop(self):
        self.running = False

class UDPBroadcaster(threading.Thread):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            message = json.dumps({"command": "hello", "peer_id": PEER_ID})
            self.sock.sendto(message.encode(), (BROADCAST_IP, UDP_PORT))
            time.sleep(5)

    def stop(self):
        self.running = False

class UDPDiscovery:
    def __init__(self):
        self.peers = set()
        self.message_history = {}

    def handle_hello_message(self, message, addr):
        print(message)
        if message.get("command") == "hello" and message.get("peer_id") != PEER_ID:
            print(f"Received hello from {message.get('peer_id')}")
            self.send_response(addr)

    def handle_response_message(self, message, addr):
        print(f"{message} at address {addr}")
        if message.get("status") == "ok" and message.get("peer_id") != PEER_ID:
            print(f"Received ok from {message['peer_id']}")

    def send_response(self, addr):
        response = json.dumps({"status": "ok", "peer_id": PEER_ID})
        self.peer_socket.sendto(response.encode(), addr)
        print(f"Sent response: {response} to {addr}")

    def start_discovery(self):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udp_socket.bind((BROADCAST_IP, UDP_PORT))
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        listener_hello = UDPListener(udp_socket, self.handle_hello_message)
        listener_hello.start()

        listener_response = UDPListener(self.peer_socket, self.handle_response_message)
        listener_response.start()

        broadcaster = UDPBroadcaster(udp_socket)
        broadcaster.start()

        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            listener_hello.stop()
            listener_response.stop()
            broadcaster.stop()

def main():
    discovery = UDPDiscovery()
    discovery.start_discovery()

if __name__ == "__main__":
    main()
