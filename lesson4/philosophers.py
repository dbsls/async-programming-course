import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
_logger = logging.getLogger("PHILOSOPHERS DINNER")

RANGE = 5
ACTION_TIME = 2


class Philosopher:

    def __init__(self, number: int, left_fork: asyncio.Lock, right_fork: asyncio.Lock, semaphore: asyncio.Semaphore):
        self.number = number
        self.name = f"Philosopher-{number}"
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.semaphore = semaphore

    async def think(self):
        _logger.debug(f"{self.name} starts thinking")
        await asyncio.sleep(ACTION_TIME)
        _logger.debug(f"{self.name} ends thinking")

    async def eat(self):
        _logger.info(f"{self.name} starts eating")
        await asyncio.sleep(ACTION_TIME)
        _logger.info(f"{self.name} ends eating")

    async def dine(self):
        _logger.info(f"{self.name} starts dine")
        while True:
            await self.think()
            async with self.semaphore:
                _logger.debug(f"{self.name} waiting for left fork")
                async with self.left_fork:
                    _logger.debug(f"{self.name} took left fork")
                    _logger.debug(f"{self.name} waiting for right fork")
                    async with self.right_fork:
                        _logger.debug(f"{self.name} took right fork")
                        await self.eat()
                        _logger.debug(f"{self.name} put right fork")
                    _logger.debug(f"{self.name} put left fork")


async def main():
    semaphore = asyncio.Semaphore(RANGE - 1)
    forks = [asyncio.Lock() for _ in range(RANGE)]
    philosophers = [Philosopher(i+1, forks[i], forks[(i+1) % 5], semaphore) for i in range(RANGE)]
    tasks = [asyncio.create_task(philosopher.dine()) for philosopher in philosophers]
    await asyncio.wait(tasks)


if __name__ == "__main__":
    asyncio.run(main())
