🛡️ RSA-Encrypted TCP Tunnel

A secure, end-to-end encrypted (E2EE) messaging tunnel built with Python. This project demonstrates the practical application of 2048-bit RSA asymmetric encryption over a reliable TCP socket connection, allowing for private communication across different networks using Ngrok for NAT traversal.  

🚀 Features

    Asymmetric Encryption: Implements 2048-bit RSA keys where only the recipient's private key can decrypt messages.  

TCP Protocol: Utilizes a connection-oriented stream to ensure data integrity and ordered packet delivery.  

NAT Traversal: Integration with Ngrok allows the tunnel to bypass residential firewalls without manual port forwarding.  

Portfolio Ready: Designed for educational analysis of encrypted traffic patterns via Wireshark.  

🛠️ Requirements

    Python 3.x  

cryptography library  

ngrok (installed on the host machine)  

Bash

pip install cryptography

📖 How It Works
1. The Secure Handshake

Upon connection, the "Host" and "Client" automatically exchange Public Keys.  

    Encryption: Messages are encrypted using the recipient's Public Key.  

Decryption: The message can only be unlocked by the recipient's Private Key, which never leaves the local device.  

2. Network Tunneling

Ngrok maps a public URL to your local port 9999. This creates a secure relay that tunnels external traffic through your firewall to your Python listener.  

🚦 Usage Instructions
Step 1: Start the Relay (Host)

In your terminal, run:
Bash

ngrok tcp 9999

Take note of the provided address (e.g., 0.tcp.au.ngrok.io:12345).  

Step 2: Launch the Listener (Host)

In a separate terminal:

    Run python3 tunnel.py.  

Select [L]isten.  

Step 3: Connect (Client)

On the remote machine:

    Run python3 tunnel.py.  

Select [C]onnect.  

Enter the Ngrok Address and Port.  

🔍 Network Analysis (Wireshark)

To verify the encryption, run Wireshark as root and filter for your tunnel port:  

Bash

sudo wireshark

Filter: tcp.port == 9999

You will observe that while the TCP structure is visible, the data payload consists of unreadable RSA-encrypted ciphertext.  

⚖️ Disclaimer

This tool is intended for educational purposes and authorized security testing only.
