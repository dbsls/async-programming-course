import json
import time

import multiprocessing as mp

import aiofiles
import asyncio

from contextlib import contextmanager
from pydantic import ValidationError
from aiofiles import os as async_os

from .schemas import CVESFile, CVEAPISchema
from .http_client import send_post_request
from .config import get_settings


@contextmanager
def timer(msg: str):
    start = time.perf_counter()
    yield
    print(f"{msg} took {time.perf_counter() - start:.2f} seconds")


async def scan_directory(path: str) -> list[str]:
    files = []
    iterator = await async_os.scandir(path)
    for el in iterator:
        if el.is_file():
            files.append(el.path)
        elif el.is_dir():
            files.extend(await scan_directory(el.path))
    return files


async def read_files(files: list[str]) -> list[CVEAPISchema]:
    result = []
    for file in files:
        async with aiofiles.open(file, mode="r") as f:
            try:
                json_data = json.loads(await f.read())
                result.append(CVEAPISchema.from_file(CVESFile(**json_data)))
            except (TypeError, json.JSONDecodeError) as e:
                print(f"Error during reading file {file}: {e}")
            except ValidationError as e:
                print(f"Error during parsing file {file}: {e}")
    return result


async def process(files: list[str]) -> None:
    with timer(f"Reading {len(files)} files"):
        results = await read_files(files)
    with timer(f"Storing {len(files)} files"):
        url = get_settings().cve_api_endpoint
        tasks = []
        for result in results:
            tasks.append(asyncio.create_task(send_post_request(url, result.model_dump())))
        print(f"CVE API tasks created: {len(tasks)}")


async def scan(path: str) -> None:
    """
    Main function.
    1. Scan directory with CVE files
    2. Read CVE files
    3. Parse CVE files to CVES database structure
    4. Save data to database
    :param path: Path to directory with CVE files
    """
    # 1. Scan directory with CVE files
    with timer("Scanning directory"):
        files = await scan_directory(path)
    print(f"Found {len(files)} files in directory {path}")

    # 2. Convert files to CVEAPI objects and cve_api app
    cpu_count = min(8, mp.cpu_count())
    count_files = len(files)
    chunk_size = count_files // cpu_count
    with timer(f"Total {count_files} files processing"):
        tasks = []
        for i in range(0, len(files), chunk_size):
            tasks.append(asyncio.create_task(process(files[i:i+chunk_size])))
        await asyncio.gather(*tasks)
