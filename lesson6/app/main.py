import json
import logging
import sys
import time

import multiprocessing as mp

import aiofiles
import asyncio

from contextlib import contextmanager
from pydantic import ValidationError

from config import get_settings
from db import CVES
from schemas import CVESFile
from aiofiles import os as async_os

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
_logger = logging.getLogger(__name__)


@contextmanager
def timer(msg: str):
    start = time.perf_counter()
    yield
    _logger.info(f"{msg} took {time.perf_counter() - start:.2f} seconds")


async def scan_directory(path: str) -> list[str]:
    files = []
    iterator = await async_os.scandir(path)
    for el in iterator:
        if el.is_file():
            files.append(el.path)
        elif el.is_dir():
            files.extend(await scan_directory(el.path))
    return files


async def read_files(files: list[str]) -> list[CVES]:
    result = []
    for file in files:
        async with aiofiles.open(file, mode="r") as f:
            try:
                json_data = json.loads(await f.read())
                result.append(CVES.from_file(CVESFile(**json_data)))
            except (TypeError, json.JSONDecodeError) as e:
                _logger.debug(f"Error during reading file {file}: {e}")
            except ValidationError as e:
                _logger.debug(f"Error during parsing file {file}: {e}")
    return result


def get_engine() -> AsyncEngine:
    settings = get_settings()
    return create_async_engine(
        settings.postgres_dsn,
        echo=settings.db_echo,
    )


def make_session_class(engine: AsyncEngine) -> type[AsyncSession]:
    return async_sessionmaker(
        engine,
        expire_on_commit=False,
    )


async def store_to_db(data: list[CVES]) -> None:
    engine = get_engine()
    session_class = make_session_class(engine)

    async with session_class() as session:
        for record in data:
            session.add(record)

        await session.flush()
        await session.commit()


async def process(files: list[str]) -> None:
    with timer(f"Reading {len(files)} files"):
        db_objs = await read_files(files)
    with timer(f"Storing {len(files)} files"):
        await store_to_db(db_objs)


async def main(path: str) -> None:
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
    _logger.info(f"Found {len(files)} files in directory {path}")

    # 2. Convert files to database objects and store to database
    cpu_count = min(8, mp.cpu_count())
    count_files = len(files)
    chunk_size = count_files // cpu_count
    with timer(f"Total {count_files} files processing"):
        tasks = []
        for i in range(0, len(files), chunk_size):
            tasks.append(asyncio.create_task(process(files[i:i+chunk_size])))
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        cves_path = sys.argv[1]
        _logger.info(f"Start process directory: {cves_path}")
        asyncio.run(main(cves_path))
    except IndexError:
        _logger.error("Script requires a path to cves directory as an argument")

