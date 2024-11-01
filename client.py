import socket
import threading

# Konfigurasi client
buffer_size = 1024

# Membuat socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(None)  # Mengatur timeout agar client tidak menunggu terlalu lama jika server tidak merespons

def get_server_info():
    while True:
        try:
            server_ip = input("Masukkan IP server: ")
            server_port = int(input("Masukkan port server: "))

            # Mengirim pesan uji coba ke server untuk memeriksa koneksi
            client_socket.sendto("PING".encode(), (server_ip, server_port))
            response, _ = client_socket.recvfrom(buffer_size)

            if response.decode() == "PONG":  # Jika server merespons, IP dan port benar
                print("Terhubung ke server!")
                return server_ip, server_port
        except socket.timeout:
            print("Tidak dapat terhubung ke server. Coba lagi.")
        except Exception as e:
            print(f"Error: {e}. Coba lagi.")

# Mendapatkan IP dan port server dengan validasi
server_ip, server_port = get_server_info()

# Proses untuk mendapatkan username dan password yang benar
while True:
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    # Mengirim permintaan JOIN ke server dengan username dan password
    client_socket.sendto(f"JOIN:{username}:{password}".encode(), (server_ip, server_port))

    # Tunggu respons apakah username dan password valid
    try:
        response, addr = client_socket.recvfrom(buffer_size)
        if response.decode() == "Password salah!" or response.decode() == "Username sudah digunakan!":
            print(response.decode())
        elif response.decode() == "Selamat datang, " + username + "!":
            print("Berhasil terhubung ke server!")
            print(response.decode())
            break  # Berhenti meminta input jika berhasil
    except socket.timeout:
        print("Tidak menerima respons dari server, coba lagi.")


# Deklarasi fungsi caesar_cipher terlebih dahulu
shift = 10 
# Shift yang akan dilakukan sebanyak 10
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

 
# Fungsi untuk menerima pesan dari server
def receive_messages():
    while True:
        try:
            # Terima pesan dari server
            data, addr = client_socket.recvfrom(buffer_size)
            response = data.decode()
            response = cipher(response, -shift)
            
            print(f"\n{response}")
        except Exception as e:
            print(f"Error saat menerima pesan: {e}")
            break

# Membuat thread untuk menerima pesan secara asinkron
threading.Thread(target=receive_messages, daemon=True).start()

# Mengirimkan pesan ke server setelah berhasil bergabung
while True:
    message = input(f"{username}: ")
    if message.lower() == "exit":
        client_socket.sendto(f"EXIT:{username}".encode() , (server_ip, server_port))
        break
    message = cipher(message, shift)
    # Mengirim pesan ke server dengan format "MSG:pesan"
    client_socket.sendto(f"MSG:{message}".encode() , (server_ip, server_port))

client_socket.close()
