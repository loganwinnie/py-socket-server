import asyncio
from config import PORT
from request_handling import build_response, handle_request

# Main Loop


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """Handle one client connection. Loops to support Keep Alive"""
    address = writer.get_extra_info("peername")

    try:
        keep_alive = True
        while keep_alive:
            try:
                head_bytes = await asyncio.wait_for(
                    reader.readuntil(b"\r\n\r\n"), timeout=60
                )
            except asyncio.IncompleteReadError:
                break
            except asyncio.TimeoutError:
                break
            try:
                response, keep_alive = handle_request(data=head_bytes)
            except ValueError as e:
                print(f"Parse error from {address}: {e}")
                response = build_response(
                    400, "Bad Request", b"<h1>400 Bad Request</h1>"
                )
                writer.write(response)
                await writer.drain()
                break

            writer.write(response)
            await writer.drain()
    except ConnectionError as e:
        print(f"Connection error from {address}: {e}")
    finally:
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass


async def main():
    server = await asyncio.start_server(handle_client, host="", port=PORT)
    print(f"Listening on port {PORT}...")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down server...")
