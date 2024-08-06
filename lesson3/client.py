import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
_logger = logging.getLogger("CLIENT")

SERVER_ADDRESS = ("localhost", 8000)

MESSAGE = "Hey, I want to know the temperature!"


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        self.transport = transport
        _logger.info(f"Sending: {self.message}")
        self.transport.write(self.message.encode())

    def data_received(self, data):
        _logger.info(f"Data received: {data.decode()}")

    def connection_lost(self, exc):
        _logger.info("The server closed the connection")
        self.on_con_lost.set_result(True)


async def main():
    loop = asyncio.get_running_loop()
    on_con_lost = loop.create_future()
    transport, protocol = await loop.create_connection(
        lambda: EchoClientProtocol(MESSAGE, on_con_lost), *SERVER_ADDRESS
    )
    try:
        await on_con_lost
    finally:
        transport.close()

if __name__ == '__main__':
    asyncio.run(main())
