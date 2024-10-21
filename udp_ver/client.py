import socket
import threading

# Konfigurasi client
server_ip = input("Masukkan IP server: ")
server_port = int(input("Masukkan port server: "))
buffer_size = 1024

# Membuat socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

username = input("Masukkan username: ")
password = input("Masukkan password: ")

# Fungsi untuk menerima pesan dari server
def receive_messages():
    while True:
        try:
            # Menerima pesan dari server
            data, addr = client_socket.recvfrom(buffer_size)
            print(f"\n{data.decode()}")
        except Exception as e:
            print(f"Error saat menerima pesan: {e}")
            break

# Mengirim permintaan JOIN ke server dengan username dan password
client_socket.sendto(f"JOIN:{username},{password}".encode(), (server_ip, server_port))

# Membuat thread untuk menerima pesan secara asinkron
threading.Thread(target=receive_messages, daemon=True).start()

# Mengirimkan pesan ke server setelah berhasil bergabung
while True:
    message = input("\nKetik pesan: ")
    if message.lower() == "exit":
        break

    # Mengirim pesan ke server dengan format "MSG:pesan"
    client_socket.sendto(f"MSG:{message}".encode(), (server_ip, server_port))

client_socket.close()
