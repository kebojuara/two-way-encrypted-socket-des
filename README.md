# Full-Duplex Two-Way Encrypted Socket Transmission using Manual Vigenere Cipher

## About

This repository contains my assignment for the Information Security course at Institut Teknologi Sepuluh Nopember, Surabaya.

The project demonstrates a real-time, two-way (full-duplex) encrypted transmission over TCP sockets. Communication is secured using a manually implemented Vigenere cipher without external cryptographic libraries. A pre-shared key (KEAMANANINFORMASI) is utilized by both endpoints and is never transmitted over the network wire.

## Features

1. Manual Cryptographic Implementation: Custom Vigenere cipher handling printable ASCII characters without relying on external cryptography libraries.
2. Full-Duplex Communication: Independent sender and receiver threads executing concurrently without blocking.
3. Cross-Platform and Multi-Device Support: Validated across physical devices (Linux/Windows workstation to Android/iOS mobile endpoints) over a local network.
4. Zero-Key Transmission: Cryptographic keys remain isolated strictly in local memory.

## Prerequisites and Installation

### 1. Ubuntu Linux

Ensure Python 3 is installed:
```bash
sudo apt update
sudo apt install python3 -y
```

### 2. Windows

1. Download and install Python from the official portal at python.org.
2. Ensure the option "Add python.exe to PATH" is checked during setup.
3. Verify the installation via Command Prompt or PowerShell:
```cmd
python --version
```

### 3. Android (Pydroid 3)

1. Install "Pydroid 3 - IDE for Python 3" directly from Google Play Store.
2. Open Pydroid 3 and paste the client.py script directly into the editor.
3. No additional terminal configuration or package installation is required.

### 4. iOS (iPhone / iPad)

1. Install "a-Shell" or "Pythonista 3" from the Apple App Store.
2. In a-Shell, Python is available out of the box. Verify by entering:
```bash
python --version
```

## Configuration: IP Address Setup

Before running the client, configure the host parameters so the client can resolve the server endpoint. Note that the default in client.py is set to 0.0.0.0 and must be replaced with the actual server IP address.

### Step 1: Identify the Server Local IP Address

On Ubuntu:
Run:
```bash
ip a
```
Locate your active wireless interface (such as wlp2s0 or wlan0) and note the IPv4 address after inet (for example 10.199.101.130).

On Windows:
Run:
```cmd
ipconfig
```
Locate the IPv4 Address under Wireless LAN adapter Wi-Fi.

### Step 2: Configure Scripts

In server.py:
Ensure HOST is bound to 0.0.0.0 to listen on all local network interfaces:
```python
HOST = '0.0.0.0'
PORT = 5000
KEY = "KEAMANANINFORMASI"
```

In client.py:
Change HOST from 0.0.0.0 to your actual server IPv4 address:
```python
HOST = '10.199.101.130'
PORT = 5000
KEY = "KEAMANANINFORMASI"
```

Both devices must be connected to the same Wi-Fi network or smartphone hotspot with client isolation disabled.

## Execution Guide

### Option 1: Ubuntu (Server) and Android Pydroid 3 (Client)

1. On Ubuntu (Server):
Allow incoming traffic on port 5000 if UFW firewall is active:
```bash
sudo ufw allow 5000/tcp
```
Start the server listener:
```bash
python3 server.py
```

2. On Android (Client via Pydroid 3):
Open Pydroid 3, paste the updated client.py script (with the server IP), and tap the yellow Play/Run button in the bottom right corner.

### Option 2: Windows (Server) and Mobile (Client)

1. On Windows (Server):
Run the server script in Command Prompt or PowerShell:
```cmd
python server.py
```
Allow network access if prompted by Windows Defender Firewall.

2. On Mobile (Client):
Run client.py targeting the Windows machine IPv4 address.

### Option 3: Single Machine Simulation (Side-by-Side Terminals)

If running both processes locally on one machine:
1. In client.py, change HOST to 127.0.0.1.
2. Open two terminal instances side by side.
3. In Terminal 1 (Server):
```bash
python3 server.py
```
4. In Terminal 2 (Client):
```bash
python3 client.py
```

## Network-Level Verification and Packet Sniffing

To prove that only encrypted ciphertext passes through the transmission medium and the secret key is never leaked, monitor network packets directly using tcpdump or Wireshark.

### Method 1: Using tcpdump (Terminal)

Open a separate terminal window and monitor the network interface handling the communication:

1. Standard Hex and ASCII Dump
```bash
sudo tcpdump -i wlp2s0 port 5000 -X -s 0
```
Replace wlp2s0 with your active network interface name, or use lo if testing on localhost.

2. Clean Payload Dump (Human Readable ASCII Only)
To filter out empty acknowledgment packets and show only the transmitted message payload:
```bash
sudo tcpdump -i wlp2s0 port 5000 -A -l -q "tcp[tcpflags] & tcp-push != 0"
```

### Method 2: Using Wireshark (Graphical Interface)

1. Installation on Ubuntu
```bash
sudo apt update && sudo apt install wireshark -y
sudo usermod -aG wireshark $USER
```

2. Capture Procedure
Start Wireshark by running:
```bash
wireshark
```
Select the active network interface (such as wlp2s0 or lo) to begin packet capture.

3. Packet Filtering
In the display filter bar at the top, enter the following filter and press Enter:
```text
tcp.port == 5000
```

4. Follow TCP Stream
Locate any packet with data length greater than zero. Right-click the packet, then navigate to Follow and select TCP Stream.
A dialog window will open displaying the full bi-directional conversation:
Client to Server payload is color-coded in red.
Server to Client payload is color-coded in blue.

### Verification Criteria

1. Transmit a known test string from the client (for example: SECRET MESSAGE).
2. Observe the captured TCP payload in either tcpdump or Wireshark.
3. Only the scrambled ciphertext bytes traverse the network.
4. The raw plaintext string is completely absent from the packet payload.
5. The pre-shared key string KEAMANANINFORMASI never traverses the wire, verifying that key storage remains strictly local.
