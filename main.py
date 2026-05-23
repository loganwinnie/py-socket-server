from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR,
)
from config import PORT
from request_handling import build_response, handle_request

# Main Loop

print("Starting server...")
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(("", PORT))
server_socket.listen(1)
print("Listening for connections...")

try:
    while True:

        client_sock, address = server_socket.accept()
        client_sock.settimeout(60)
        try:
            received = client_sock.recv(4096)
            response = handle_request(received)
            client_sock.send(response)
        except (ValueError, ConnectionError, TimeoutError) as e:
            print(f"Error handling client {address}: {e}")
            try:
                client_sock.send(
                    build_response(400, "Bad Request", "<h1>400 Bad Request</h1>")
                )
            except Exception:
                # Client has disconnected
                pass
        finally:
            client_sock.close()
except KeyboardInterrupt:
    print("Shutting down server...")
finally:
    server_socket.close()
