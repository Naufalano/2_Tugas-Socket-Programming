import socket
import threading

# Konfigurasi server
server_ip = "127.0.0.1"
server_port = 12345
buffer_size = 1024

# Membuat socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

print(f"Server aktif di {server_ip}:{server_port}")

clients = set()

# Fungsi untuk menangani client dan broadcast pesan
def handle_client():
    while True:
        try:
            data, addr = server_socket.recvfrom(buffer_size)
            
            # Tambahkan client baru ke set clients
            if addr not in clients:
                clients.add(addr)
                print(f"Client baru terhubung: {addr}")

            # Menampilkan pesan yang diterima di server
            print(f"Pesan dari {addr}: {data.decode()}")

            # Broadcast pesan ke semua client selain pengirim
            for client in clients:
                if client != addr:  # Jangan kirim kembali ke pengirim
                    server_socket.sendto(data, client)
                    print(f"Pesan diteruskan ke {client}")
                else:
                    print(f"Pesan tidak dikirim kembali ke pengirim: {client}")
        except Exception as e:
            print(f"Error: {e}")
            continue

# Menjalankan server dalam thread agar bisa menangani banyak client
threading.Thread(target=handle_client, daemon=True).start()

while True:
    pass
