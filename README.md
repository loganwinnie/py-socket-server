# py-socket-server

A from scratch HTTP/1.1 server built from scratch in Python using only the standard library's socket module. 

## Status
 
Server now parses HTTP requests and serves valid response with routing, static file serving, path protection, status codes, and error handling.

## What works today

- A from-scratch HTTP/1.1 server
- Routing, status codes, content-type detection
- Static file serving with path-traversal protection
- HTTP Keep-Alive (one TCP connection, many requests)
- Asyncio-based concurrency (one thread, many simultaneous clients)
- An event-driven I/O model you can articulate
- 

## Run it
```bash
python main.py
```

## Test it
```bash
curl -v http://localhost:8080/hello
```

