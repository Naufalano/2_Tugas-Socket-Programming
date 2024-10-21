import socket
import threading

# Konfigurasi server
server_ip = "127.0.0.1"
server_port = 12345
buffer_size = 1024
password = "secretpassword"  # Password chat room

# Membuat socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

print(f"Server aktif di {server_ip}:{server_port}")

clients = {}
usernames = set()
message_id = 0  # Untuk melacak nomor urut pesan

# Fungsi untuk menangani pesan dari client
def handle_client():
    global message_id
    while True:
        try:
            data, addr = server_socket.recvfrom(buffer_size)
            message = data.decode().split(":", 2)

            if message[0] == "JOIN":
                username, client_password = message[1].split(",")

                # Verifikasi password
                if client_password.strip() == password:
                    if username not in usernames:
                        usernames.add(username)
                        clients[addr] = username
                        print(f"{username} telah bergabung dari {addr}")
                        server_socket.sendto(f"Selamat datang, {username}!".encode(), addr)
                    else:
                        server_socket.sendto(f"Username {username} sudah digunakan!".encode(), addr)
                else:
                    server_socket.sendto("Password salah!".encode(), addr)

            elif message[0] == "MSG":
                username = clients.get(addr, None)
                if username:
                    # Broadcast pesan ke semua client selain pengirim dengan nomor urut pesan
                    message_id += 1
                    broadcast_message = f"{message_id}:{username}:{message[1]}"
                    print(f"Menerima pesan dari {username}: {message[1]} (ID: {message_id})")

                    # Broadcast pesan ke semua client
                    for client in clients:
                        if client != addr:
                            server_socket.sendto(broadcast_message.encode(), client)
                            print(f"Pesan {message_id} diteruskan ke {client}")

        except Exception as e:
            print(f"Error: {e}")
            continue

# Menjalankan server dalam thread agar bisa menangani banyak client
threading.Thread(target=handle_client, daemon=True).start()

while True:
    pass
