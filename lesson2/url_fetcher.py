import os
import sys
import logging
import asyncio
import aiofiles

from typing import Any
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectionError

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

FETCHING_RESULTS_DIR = "fetching_results"

FETCH_TIMEOUT = 3
SAVE_TO_FILE_TIMEOUT = 0.2


def ensure_dir_exists(f_name: str) -> None:
    fetching_results_destination = f"{FETCHING_RESULTS_DIR}/{f_name}"
    directory = os.path.dirname(fetching_results_destination)
    if directory and not os.path.exists(FETCHING_RESULTS_DIR) and not os.path.exists(fetching_results_destination):
        os.makedirs(FETCHING_RESULTS_DIR)


def get_new_file_name(url: str) -> str:
    for i in ['https://', 'http://', 'www.']:
        url = url.replace(i, '')
    url = url.replace("/", "_")
    return f"{url}.html"


async def save_to_file(url: str, data: str) -> None:
    f_name = get_new_file_name(url)
    ensure_dir_exists(f_name)
    file = f"{FETCHING_RESULTS_DIR}/{f_name}"
    try:
        async with aiofiles.open(file, mode="w") as f:
            await asyncio.wait_for(f.write(data), timeout=SAVE_TO_FILE_TIMEOUT)
        _logger.info(f"URL: [{url}] - Results were saved to {file}")
    except asyncio.TimeoutError:
        _logger.warning(f"Results from [{url}] were not saved to file because of timeout, saving task canceled")
    except FileNotFoundError as e:
        _logger.error(f"File [{file}] not found error: {e}")
    except Exception as e:
        _logger.error(f"An error occurred during results saving to {file}: {e}")


async def process_results(results: tuple[Any]) -> None:
    process_tasks = []
    for url, data in results:
        process_tasks.append(
            asyncio.create_task(save_to_file(url, data))
        )
    await asyncio.gather(*process_tasks)


async def fetch_url(url: str) -> str:
    async with ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def run_fetching(url: str) -> tuple:
    _logger.info(f"Fetching url: {url}")
    try:
        async with asyncio.timeout(FETCH_TIMEOUT):
            result = await fetch_url(url)
    except asyncio.TimeoutError:
        error_msg = f"Timeout error occurred during fetching: {url}"
        _logger.error(error_msg)
        result = error_msg
    except ClientConnectionError as e:
        error_msg = f"Error occurred during fetching: {e}"
        _logger.error(error_msg)
        result = error_msg
    return url, result


async def create_tasks(file: str) -> list:
    tasks = []
    try:
        async with aiofiles.open(file, mode="r") as f:
            _logger.info(f"Start reading file {file}")
            async for line in f:
                tasks.append(
                    asyncio.create_task(run_fetching(str(line).strip()))
                )
    except FileNotFoundError:
        _logger.error(f"File {file} not found.")
    _logger.info(f"{len(tasks)} tasks were created from file {file}")
    return tasks


async def main(file: str) -> None:
    _logger.info("Run...")
    tasks = await create_tasks(file)
    results = await asyncio.gather(*tasks)
    await process_results(results)
    _logger.info("Finished!")

if __name__ == "__main__":
    try:
        f_path = sys.argv[1]
        asyncio.run(main(f_path))
    except IndexError:
        _logger.error("Script requires a file as an argument")
