import socket
import threading

# Konfigurasi client
server_ip = "127.0.0.1"
server_port = 12345
buffer_size = 1024

# Membuat socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Fungsi untuk menerima pesan dari server
def receive_messages():
    while True:
        try:
            # Menerima pesan dari server
            data, addr = client_socket.recvfrom(buffer_size)
            print(f"Pesan baru dari server: {data.decode()} (dari {addr})")
        except Exception as e:
            print(f"Error saat menerima pesan: {e}")
            break

# Membuat thread untuk menerima pesan secara asinkron
threading.Thread(target=receive_messages, daemon=True).start()

# Mengirimkan pesan ke server dan broadcast ke client lain
while True:
    message = input("Ketik pesan: ")
    if message.lower() == "exit":
        break
    
    # Mengirim pesan ke server
    client_socket.sendto(message.encode(), (server_ip, server_port))
    print(f"Pesan terkirim ke server: {message}")

client_socket.close()
