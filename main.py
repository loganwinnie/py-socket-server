from dataclasses import dataclass
from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR,
)
from config import PORT

ROUTES = {
    "/": "<h1>Welcome</h1><p>This server was built from scratch.</p>",
    "/hello": "<h1>Hello, World!</h1>",
    "/about": "<h1>About</h1><p>Day 3 of a 7-day build.</p>",
}


# Class definitions
@dataclass
class Request:
    method: str
    path: str
    version: str
    headers: dict[str, str]


def parse_request(data: bytes) -> Request:
    request_line, request_rest = data.decode().split("\r\n", 1)
    header_block, _ = request_rest.split("\r\n\r\n", 1)

    # parse request line
    split_request_line = request_line.split(" ", 2)
    if len(split_request_line) != 3:
        raise ValueError(f"Malformed request line: {request_line!r}")
    method, path, version = split_request_line
    # parse headers

    headers = {}
    header_line = header_block.split("\r\n")
    for header in header_line:
        if header == "":
            break

        split_header = header.split(":", 1)
        if len(split_header) != 2:
            raise ValueError(f"Malformed header: {header!r}")
        name, value = split_header
        name = name.strip().lower()
        value = value.strip()
        headers[name] = value

    return Request(method, path, version, headers)


# Response Functions
def build_response(
    status_code: int, status_text: str, body: str, content_type: str = "text/html"
) -> bytes:
    body_bytes = body.encode()
    response = (
        f"HTTP/1.1 {status_code} {status_text}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "\r\n"
        f"{body}"
    )
    return response.encode()


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
            parsed_request = parse_request(received)
            print(
                f"\n{address[0]}:{address[1]} - {parsed_request.method} {parsed_request.path}\n"
            )
            if parsed_request.method != "GET":
                response = build_response(
                    405,
                    "Method Not Allowed",
                    f"<h1>{parsed_request.method} Method Not Allowed</h1>",
                )
            elif parsed_request.path in ROUTES:
                response = build_response(200, "OK", ROUTES[parsed_request.path])
            else:
                response = build_response(404, "Not Found", "<h1>404 Not Found</h1>")

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
