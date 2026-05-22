# py-socket-server

A from scratch HTTP/1.1 server built from scratch in Python using only the standard library's socket module. 

## Status
 
Server now parses HTTP requests and serves valid response with routing, status codes, and error handling.

## What works today

- Single-client TCP server on a configurable port.
- Graceful handling of client disconnects.
- 60-second idle timeout.
- Clean shutdown on client close.
- Server parses HTTP requests and serves valid response.
- Super basic routing and error handling. 
- Handles request and serves robust response

## Run it
```bash
python main.py
```

## Test it
```bash
curl -v http://localhost:8080/hello
```

