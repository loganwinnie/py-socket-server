# py-socket-server

A from scratch HTTP/1.1 server built from scratch in Python using only the standard library's socket module. 

## Status
 
The TCP layer is working, the server is accepting connections and echoes bytes back.

## What works today

- Single-client TCP server on a configurable port
- Graceful handling of client disconnects
- 60-second idle timeout
- Clean shutdown on client close

## Run it
```bash
python main.py
```

## Test it
```bash
nc localhost 8080 
hello <-- Any message 
hello <-- message echoed back
```

