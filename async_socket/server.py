#!/usr/bin/env python

import asyncio

HOST = "127.0.0.1"
PORT = 5510


async def handle_echo(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    data = None
    while data != b"quit":
        data = await reader.read(1024)
        msg = data.decode()
        addr, port = writer.get_extra_info("peername")
        print(f"Received message from {addr}:{port}: {msg!r}")
        writer.write(data)
        await writer.drain()
    writer.close()
    await writer.wait_closed()


async def run_server():
    server = await asyncio.start_server(handle_echo, HOST, PORT)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_server())
