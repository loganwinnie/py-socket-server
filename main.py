from dataclasses import dataclass
from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR,
)
from config import PORT


@dataclass
class RequestLine:
    method: str
    path: str
    version: str


def parse_request_line(data: bytes) -> RequestLine:
    request_line, _ = data.decode().split("\r\n", 1)
    parts = request_line.split(" ", 2)
    if len(parts) != 3:
        raise ValueError(f"Malformed request line: {request_line!r}")
    method, path, version = parts
    return RequestLine(method, path, version)


def parse_headers(data: bytes) -> dict[str, str]:
    header_block, _ = data.decode().split("\r\n\r\n", 1)
    lines = header_block.split("\r\n")

    headers = {}
    for header in lines[1:]:
        if header == "":
            break

        split_header = header.split(":", 1)
        if len(split_header) != 2:
            raise ValueError(f"Malformed header: {header!r}")
        name, value = split_header
        name = name.strip().lower()
        value = value.strip()
        headers[name] = value
    return headers


print("Starting server...")
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(("", PORT))
server_socket.listen(1)
print("Listening for connections...")

client_sock, address = server_socket.accept()
client_sock.settimeout(60)
print(f"connected at {address}")

received = client_sock.recv(4096)

print("=== REQUEST ===")
parsed_request_line = parse_request_line(received)
parsed_header = parse_headers(received)
print(parsed_request_line)
print(parsed_header)
print("=== END ===")

response = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html\r\n"
    "Content-Length: 13\r\n"
    "\r\n"
    "Hello, World!"
)

client_sock.send(response.encode())

client_sock.close()
server_socket.close()
