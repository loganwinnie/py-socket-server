 # pysock

 An HTTP/1.1 server built from scratch in Python no `http.server`, no frameworks.
 Just the `socket` layer, `asyncio`, and the standard library.

 It started as a build to understand project. 

 ## Why

 `http.server` hands you a working server and hides the interesting parts. pysock
 doesn't: it parses the request line and headers by hand, assembles the response bytes by hand, and handles concurrency with a single-threaded event loop you can read end to end. ~200 lines, zero dependencies.

 ## Architecture

 One thread, one event loop, many simultaneous clients. Every request runs the
 same
 path:

 ```
 read  ->  parse  ->  route  ->  static file  ->  404
 ```

 - **`main.py`**  the asyncio server. Binds the socket, accepts connections,
 runs the per-connection keep-alive loop.
 - **`request_handling.py`** everything HTTP: request parsing, the route table,
   static file serving, status codes, content-type detection.
 - **`config.py`** the port lives here.

 Dispatch order per request: check the route table first, fall back to a static
 file
 under `public/`, otherwise 404.

 ## What works today

 - HTTP/1.1 request parsing,  request line, headers, by hand
 - Routing via a simple table (`/hello`, `/about`)
 - Static file serving from `public/`, with path-traversal protection (resolved
   paths must stay under the public root)
 - Content-type detection by extension
 - Status codes: 200, 400, 404, 405
 - Keep-Alive, one TCP connection, many requests, with a 60s idle timeout
 - Asyncio concurrency
 - Graceful shutdown

 ## Not yet (on purpose)

 GET-only and header-only for now enough to serve pages and reason about the
 protocol, not to run in production.

 - GET only (everything else gets a clean 405)
 - No request-body parsing
 - No TLS, compression, or chunked transfer encoding
 - No cookies or sessions
 - Static file reads are still blocking inside the async handler

 ## Roadmap

 - Request bodies + POST
 - Async file I/O so large files don't stall the loop
 - More of the method surface (HEAD, OPTIONS)
 - A few tests against the parser and the traversal guard

# Quickstart

 ## Run it

 ```bash
 git clone git@github.com:loganwinnie/pysock.git
 python main.py
 ```

### With Docker
```bash
docker build -t pysock .
docker run -p 8080:8080 pysock
```
Then visit http://localhost:8080

 ## Test it

 ```bash
 curl -v http://localhost:8080/hello   # routed
 curl -v http://localhost:8080/        # serves public/index.html
 curl -v http://localhost:8080/nope    # 404
 ```
