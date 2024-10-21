import socket
import threading
import time

# Konfigurasi client
server_ip = input("Masukkan IP server: ")
server_port = int(input("Masukkan port server: "))
buffer_size = 1024

# Membuat socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

username = input("Masukkan username: ")
password = input("Masukkan password: ")

received_messages = set()  # Untuk melacak pesan yang sudah diterima

# Fungsi untuk menerima pesan dari server
def receive_messages():
    while True:
        try:
            # Menerima pesan dari server
            data, addr = client_socket.recvfrom(buffer_size)
            message_parts = data.decode().split(":", 2)
            message_id = int(message_parts[0])  # Nomor urut pesan
            sender = message_parts[1]
            message = message_parts[2]

            # Jika pesan belum diterima, terima dan kirim ACK
            if message_id not in received_messages:
                received_messages.add(message_id)
                print(f"\n{sender}: {message} (ID: {message_id})")

                # Kirim ACK ke server
                client_socket.sendto(f"ACK:{message_id}".encode(), (server_ip, server_port))

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
