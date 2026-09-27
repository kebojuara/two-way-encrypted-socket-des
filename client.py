import socket
import threading
import sys

# Konfigurasi Jaringan & Kunci (Ganti Sesuai IP Server)
HOST = '0.0.0.0'
PORT = 5000
KEY = "KEAMANANINFORMASI"

def vigenere_encrypt(plaintext, key):
    ciphertext = []
    for i, char in enumerate(plaintext):
        k = key[i % len(key)]
        encrypted_char = chr((ord(char) - 32 + (ord(k) - 32)) % 95 + 32)
        ciphertext.append(encrypted_char)
    return "".join(ciphertext)

def vigenere_decrypt(ciphertext, key):
    plaintext = []
    for i, char in enumerate(ciphertext):
        k = key[i % len(key)]
        decrypted_char = chr((ord(char) - 32 - (ord(k) - 32)) % 95 + 32)
        plaintext.append(decrypted_char)
    return "".join(plaintext)

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            if not data:
                print("\n[INFO] Koneksi ditutup oleh Server.")
                break
            
            decrypted = vigenere_decrypt(data, KEY)
            print(f"\n[MASUK] Ciphertext diterima : {data}")
            print(f"[MASUK] Plaintext terdekripsi: {decrypted}")
            print("Anda: ", end="", flush=True)
        except Exception:
            break
    sock.close()
    sys.exit()

def send_messages(sock):
    while True:
        try:
            message = input("Anda: ")
            if not message.strip():
                continue
            
            ciphertext = vigenere_encrypt(message, KEY)
            print(f"[KELUAR] Ciphertext terkirim : {ciphertext}")
            sock.sendall(ciphertext.encode('utf-8'))
        except (KeyboardInterrupt, EOFError):
            print("\n[INFO] Menutup koneksi...")
            sock.close()
            sys.exit()

def main():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_sock.connect((HOST, PORT))
    except ConnectionRefusedError:
        print(f"[ERROR] Gagal terhubung ke {HOST}:{PORT}. Pastikan server.py sudah berjalan!")
        sys.exit(1)

    print(f"[CLIENT] Terhubung ke Server di {HOST}:{PORT}!")
    print("------------------------------------------------------------")

    # Menjalankan thread simultan
    recv_thread = threading.Thread(target=receive_messages, args=(client_sock,), daemon=True)
    send_thread = threading.Thread(target=send_messages, args=(client_sock,))

    recv_thread.start()
    send_thread.start()

    send_thread.join()
    client_sock.close()

if __name__ == '__main__':
    main()