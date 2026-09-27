import socket
import threading
import sys

# Konfigurasi Jaringan & Kunci
HOST = '0.0.0.0'
PORT = 5000
KEY = "KEAMANANINFORMASI"

def vigenere_encrypt(plaintext, key):
    ciphertext = []
    for i, char in enumerate(plaintext):
        k = key[i % len(key)]
        # Pergeseran modular berbasis rentang ASCII printable (32 hingga 126, total 95 karakter)
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
                print("\n[INFO] Koneksi ditutup oleh Client.")
                break
            
            decrypted = vigenere_decrypt(data, KEY)
            # Menampilkan ciphertext yang diterima dari jaringan dan hasil dekripsinya
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
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(1)

    print(f"[SERVER] Menunggu koneksi dari Client di {HOST}:{PORT}...")
    conn, addr = server_sock.accept()
    print(f"[SERVER] Terhubung dengan {addr}!")
    print("------------------------------------------------------------")

    # Menjalankan thread untuk menerima dan mengirim data secara simultan
    recv_thread = threading.Thread(target=receive_messages, args=(conn,), daemon=True)
    send_thread = threading.Thread(target=send_messages, args=(conn,))

    recv_thread.start()
    send_thread.start()

    send_thread.join()
    conn.close()
    server_sock.close()

if __name__ == '__main__':
    main()