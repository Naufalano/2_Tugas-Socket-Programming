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

# Fungsi untuk menangani pesan dari client dan broadcast ke client lain
def handle_client():
    while True:
        try:
            # Terima pesan dari client
            data, addr = server_socket.recvfrom(buffer_size)
            message = data.decode()

            # Memproses pesan PING dan mengirim PONG sebagai respons
            if message == "PING":
                print(f"Pesan PING diterima dari {addr}, mengirim PONG...")
                server_socket.sendto("PONG".encode(), addr)
                continue

            # Proses JOIN: memisahkan username dan password
            if message.startswith("JOIN"):
                _, username, client_password = message.split(":")

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
            elif message.startswith("MSG"):
                username = clients.get(addr, None)
                if username:
                    # Broadcast pesan ke semua client selain pengirim
                    broadcast_message = f"{username}: {message.split(':', 1)[1]}"
                    print(f"Menerima pesan dari {username}: {message.split(':', 1)[1]}")

                    # Kirim ke semua client yang terhubung
                    for client in clients:
                        if client != addr:
                            server_socket.sendto(broadcast_message.encode(), client)

        except Exception as e:
            print(f"Error: {e}")
            continue

# Menjalankan server dalam thread agar bisa menangani banyak client
threading.Thread(target=handle_client, daemon=True).start()

while True:
    pass
