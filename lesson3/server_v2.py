import asyncio
import logging
from thermometer import Thermometer


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
_logger = logging.getLogger("SERVER-V2")

SERVER_ADDRESS = ("localhost", 8000)
DEFAULT_DELAY = 2


class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        _logger.info(f"Connection from {self.address}")
        asyncio.create_task(self.stream_data())

    def data_received(self, data):
        _logger.info(f"Data received from [{self.address}]: {data.decode()}")

    def connection_lost(self, exc):
        _logger.info(f"Connection lost with {self.address}")

    async def stream_data(self):
        thermometer = Thermometer()
        last_temp = None
        while True:
            current_temp = await thermometer.get_temperature()
            if current_temp != last_temp:
                last_temp = current_temp
                message = f"Current temperature is {current_temp} degrees"
                _logger.info(f"Send to [{self.address}] message: {message}")
                self.transport.write(message.encode())
            await asyncio.sleep(DEFAULT_DELAY)


async def main():
    task = asyncio.create_task(Thermometer().run_measures())
    _logger.info(f"Run temperature measuring task in background: {task.get_name()}")
    loop = asyncio.get_running_loop()
    server = await loop.create_server(lambda: EchoServerProtocol(), *SERVER_ADDRESS)
    _logger.info("Server started")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
