import asyncio
import logging
import random


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
_logger = logging.getLogger("THERMOMETER")

MEASURE_PERIOD = 2


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Thermometer(metaclass=SingletonMeta):
    _temperature = None

    @staticmethod
    def get_random_temperature(latest_temp: int = 18) -> int:
        return random.randint(latest_temp - 2, latest_temp + 2)

    async def run_measures(self):
        while True:
            current_temp = self.get_random_temperature(self._temperature or 18)
            if current_temp != self._temperature:
                _logger.debug(f"Current temperature is {current_temp} degrees")
            self._temperature = current_temp
            await asyncio.sleep(MEASURE_PERIOD)

    async def get_temperature(self):
        if self._temperature is None:
            self._temperature = self.get_random_temperature()
        return self._temperature
