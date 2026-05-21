from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR,
)
from config import PORT

print("Starting server...")
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(("", PORT))
server_socket.listen(1)
print("Listening for connections...")

client_sock, address = server_socket.accept()
client_sock.settimeout(60)
print(f"connected at {address}")

while True:
    received = client_sock.recv(1024)

    if received == b"":
        print("Client disconnected")
        break

    client_sock.send(received)

client_sock.close()
server_socket.close()
print("Server closed")
