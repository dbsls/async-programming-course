import asyncio
import logging
from thermometer import Thermometer


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
_logger = logging.getLogger("SERVER-V1")

SERVER_ADDRESS = ("localhost", 8000)
READ_LIMIT = 100
DEFAULT_DELAY = 2


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    data = await reader.read(READ_LIMIT)
    message = data.decode()
    addr = writer.get_extra_info("peername")
    _logger.info(f"Received message from {addr}: {message}")

    try:
        thermometer = Thermometer()
        last_temp = None
        while True:
            current_temp = await thermometer.get_temperature()
            if current_temp != last_temp:
                last_temp = current_temp
                msg = f"Current temperature: {current_temp}"
                _logger.info(f"Send to [{addr}] message: {msg}")
                writer.write(msg.encode())
                await writer.drain()
            await asyncio.sleep(DEFAULT_DELAY)
    except ConnectionResetError as e:
        _logger.warning(f"Closing the connection with : [{addr}]")
        writer.close()


async def main():
    task = asyncio.create_task(Thermometer().run_measures())
    _logger.info(f"Run temperature measuring task in background: {task.get_name()}")
    server = await asyncio.start_server(handle_client, *SERVER_ADDRESS)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
