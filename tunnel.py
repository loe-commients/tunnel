import socket
import threading
import sys
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

class SecureTunnel:
    def __init__(self, port=9999):
        self.port = port
        # SWITCHED TO TCP (SOCK_STREAM)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()
        self.peer_pub_key = None
        self.conn = None

    def get_own_pub_pem(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def encrypt(self, message):
        return self.peer_pub_key.encrypt(
            message.encode(),
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), 
                         algorithm=hashes.SHA256(), label=None)
        )

    def decrypt(self, ciphertext):
        return self.private_key.decrypt(
            ciphertext,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), 
                         algorithm=hashes.SHA256(), label=None)
        ).decode()

    def listen(self):
        # Allow port reuse to avoid "Address already in use" errors
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.listen(1)
        print(f"[LISTENING] Tunnel active on port {self.port}. Waiting for Ngrok...")
        
        self.conn, addr = self.sock.accept()
        print(f"[CONNECTED] Ngrok relayed a connection from {addr}")
        
        # RSA Handshake
        self.conn.send(self.get_own_pub_pem())
        data = self.conn.recv(4096)
        self.peer_pub_key = serialization.load_pem_public_key(data)
        print("[SECURE] Public keys exchanged over TCP.")

    def connect(self, ip, port):
        print(f"[CONNECTING] Reaching out to {ip}:{port}...")
        self.sock.connect((ip, port))
        self.conn = self.sock
        
        # RSA Handshake
        data = self.conn.recv(4096)
        self.peer_pub_key = serialization.load_pem_public_key(data)
        self.conn.send(self.get_own_pub_pem())
        print("[SECURE] Public keys exchanged over TCP.")

    def receiver(self):
        while True:
            try:
                data = self.conn.recv(4096)
                if not data: break
                decrypted = self.decrypt(data)
                print(f"\n[PARTNER]: {decrypted}\n> ", end="")
            except Exception as e:
                print(f"\n[ERROR] Connection lost: {e}")
                break

def run():
    print("--- Python TCP Secure Tunnel ---")
    mode = input("Select Mode: [L]isten or [C]onnect: ").lower()
    tunnel = SecureTunnel()

    if mode == 'l':
        tunnel.listen()
    elif mode == 'c':
        target_addr = input("Enter Ngrok Address (e.g., 0.tcp.au.ngrok.io): ")
        target_port = int(input("Enter Ngrok Port (e.g., 12345): "))
        tunnel.connect(target_addr, target_port)
    else:
        return

    threading.Thread(target=tunnel.receiver, daemon=True).start()

    while True:
        msg = input("> ")
        if msg.lower() in ['exit', 'quit']: break
        if msg:
            try:
                self_encrypted = tunnel.encrypt(msg)
                tunnel.conn.send(self_encrypted)
            except Exception as e:
                print(f"Failed to send: {e}")
                break

if __name__ == "__main__":
    run()
