import socket
import threading

# Konfigurasi server
server_ip = "127.0.0.1"
server_port = 23456
buffer_size = 1024
password = "secretpassword"  # Password chat room

# Membuat socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

print(f"Server aktif di {server_ip}:{server_port}")

clients = {}
usernames = set()

# Fungsi untuk menangani pesan dari client
def handle_client():
    while True:
        try:
            data, addr = server_socket.recvfrom(buffer_size)
            message = data.decode().split(":", 1)

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
                    broadcast_message = f"{username}: {message[1]}"
                    print(f"Menerima pesan dari {username}: {message[1]}")

                    # Broadcast pesan ke semua client kecuali pengirim
                    for client_addr in clients:
                        if client_addr != addr:
                            server_socket.sendto(broadcast_message.encode(), client_addr)
                            print(f"Pesan diteruskan ke {client_addr}")

        except Exception as e:
            print(f"Error: {e}")
            continue

# Menjalankan server dalam thread agar bisa menangani banyak client
threading.Thread(target=handle_client, daemon=True).start()

while True:
    pass
