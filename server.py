import socket
import threading

# Konfigurasi server
server_ip = "127.0.0.1"
server_port = 12345
buffer_size = 1024
password = "secretpassword"  # Password yang benar untuk masuk ke chatroom

# Membuat socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

print(f"Server aktif di {server_ip}:{server_port}")

clients = {}  # Menyimpan alamat client dan username yang terhubung
usernames = set()

# Fungsi untuk caesar cipher
shift = 10
def cipher(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha(): #Jika alfabet, geser
            shift_amount = shift % 26
            if char.islower():
                encrypted_text += chr((ord(char) - ord('a') + shift_amount) % 26 + ord('a'))
            elif char.isupper():
                encrypted_text += chr((ord(char) - ord('A') + shift_amount) % 26 + ord('A'))
        else:
            encrypted_text += char
    return encrypted_text

# Fungsi untuk menangani pesan dari client dan broadcast ke client lain
def handle_client():
    while True:
        try:
            data, addr = server_socket.recvfrom(buffer_size)
            message = data.decode()

            # Memproses pesan PING dan mengirim PONG sebagai respons
            if message == "PING":
                print(f"Pesan PING diterima dari {addr}, mengirim PONG...")
                server_socket.sendto("PONG".encode(), addr)
                continue
            
            message = message.split(":", 1)
            # Proses JOIN: memisahkan username dan password
            if message[0] == "JOIN":
                username, client_password = message[1].split(":")

                # Verifikasi password
                if client_password.strip() != password:
                    server_socket.sendto("Password salah!".encode(), addr)
                    continue  # Kembali meminta client memasukkan password

                # Verifikasi username unik
                if username in clients.values():
                    server_socket.sendto("Username sudah digunakan!".encode(), addr)
                    continue  # Kembali meminta client memasukkan username

                # Tambahkan client ke daftar jika password dan username valid
                clients[addr] = username
                print(f"{username} telah bergabung dari {addr}")
                server_socket.sendto(f"Selamat datang, {username}!".encode(), addr)

            # Proses MSG: kirim pesan ke semua client lain
            elif message[0] == "MSG":
                username = clients.get(addr, None)
                if username:
                    # Broadcast pesan ke semua client selain pengirim
                    
                    broadcast_message = f"{cipher(username, shift)}: {message[1]}"
                    print(f"Menerima pesan dari {username}: {message[1]}")

                    # Kirim ke semua client yang terhubung
                    for client_addr in clients:
                        if client_addr != addr:  # Jangan kirim ke pengirim
                            server_socket.sendto(broadcast_message.encode(), client_addr)
                            print(f"Pesan dikirim ke {client_addr}")

        except Exception as e:
            print(f"Error: {e}")
            continue

# Menjalankan server dalam thread agar bisa menangani banyak client
threading.Thread(target=handle_client, daemon=True).start()

while True:
    pass
