from dataclasses import dataclass
from pathlib import Path

PUBLIC_DIR = Path("public")

ROUTES = {
    "/hello": "<h1>Hello, World!</h1>",
    "/about": "<h1>About</h1><p>Day 3 of a 7-day build.</p>",
}

CONTENT_TYPES = {
    ".html": "text/html",
    ".css": "text/css",
    ".js": "application/javascript",
    ".json": "application/json",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".txt": "text/plain",
}


# Class definitions
@dataclass
class Request:
    method: str
    path: str
    version: str
    headers: dict[str, str]


# Parsing
def parse_request(data: bytes) -> Request:
    request_line, request_rest = data.decode("utf-8", errors="strict").split("\r\n", 1)
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


def content_type_for(path: Path) -> str:
    """Hand rolled content type table getter for given path. Could use stdlib(mimetypes) for larger table"""
    return CONTENT_TYPES.get(path.suffix.lower(), "application/octet-stream")


# Response Functions
def build_response(
    status_code: int,
    status_text: str,
    body: str | bytes,
    content_type: str = "text/html",
) -> bytes:
    body_bytes = body.encode() if isinstance(body, str) else body

    head = (
        f"HTTP/1.1 {status_code} {status_text}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "\r\n"
    )
    return head.encode() + body_bytes


# Request Handling & Routing
def handle_routes(req: Request) -> bytes | None:
    """Try the route table. Return response bytes or None if no match."""
    if req.path in ROUTES:
        return build_response(200, "OK", ROUTES[req.path])
    return None


def handle_file_path(req: Request) -> bytes | None:
    """Try to serve a file from the public directory. Return None if not found."""
    path = req.path.strip("/")
    if path == "":
        path = "index.html"
    file_path = Path(PUBLIC_DIR, path).resolve()
    public_root = PUBLIC_DIR.resolve()

    if not file_path.is_file() or not file_path.is_relative_to(public_root):
        return None

    return build_response(
        200,
        "OK",
        file_path.read_bytes(),
        content_type=content_type_for(file_path),
    )


def handle_not_found() -> bytes:
    """Final fallback. Always returns a 'Not Found' response."""
    return build_response(404, "Not Found", "<h1>404 Not Found</h1>")


def handle_request(data: bytes) -> bytes:
    """Dispatch request to handler that can serve the request"""

    request = parse_request(data)

    if request.method != "GET":
        return build_response(
            405, "Method Not Allowed", f"<h1>405 Method Not Allowed</h1>"
        )

    response = handle_routes(request)
    if response is not None:
        return response

    response = handle_file_path(request)
    if response is not None:
        return response

    return handle_not_found()
