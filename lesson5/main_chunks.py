import asyncio
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from functions import process_file_chunk
from main import timer, reduce_words, monitoring


FILE_PATH = "./googlebooks-eng-all-1gram-20120701-a"
WORD = "ära"


def get_file_chunks(
    file_name: str,
    max_cpu: int = 8,
) -> tuple[int, list[tuple[str, int, int]]]:
    """Split file into chunks"""
    import os
    import multiprocessing as mp

    # Determine the number of CPUs to use
    cpu_count = min(max_cpu, mp.cpu_count())

    # Calculate the size of each chunk
    file_size = os.path.getsize(file_name)
    chunk_size = file_size // cpu_count

    start_end = list()
    with open(file_name, mode="r+b") as f:

        def is_new_line(position):
            if position == 0:
                return True
            else:
                f.seek(position - 1)
                return f.read(1) == b"\n"

        def next_line(position):
            f.seek(position)
            f.readline()
            return f.tell()

        chunk_start = 0
        while chunk_start < file_size:
            chunk_end = min(file_size, chunk_start + chunk_size)

            while not is_new_line(chunk_end):
                chunk_end -= 1

            if chunk_start == chunk_end:
                chunk_end = next_line(chunk_end)

            start_end.append(
                (
                    file_name,
                    chunk_start,
                    chunk_end,
                )
            )

            chunk_start = chunk_end

    return (
        cpu_count,
        start_end,
    )


async def main():
    loop = asyncio.get_event_loop()

    words = {}

    with timer("Reading file"):
        _, chunks = get_file_chunks(FILE_PATH)

    with mp.Manager() as manager:
        counter = manager.Value("i", 0)
        counter_lock = manager.Lock()

        monitoring_task = asyncio.shield(
            asyncio.create_task(monitoring(counter, counter_lock, chunks[-1][2]))
        )

        with ProcessPoolExecutor() as executor:
            with timer("Processing data"):
                results = []
                for chunk in chunks:
                    results.append(
                        loop.run_in_executor(
                            executor,
                            process_file_chunk,
                            *chunk,
                            counter,
                            counter_lock,
                        )
                    )

                done, _ = await asyncio.wait(results)

        monitoring_task.cancel()

    with timer("Reducing results"):
        for result in done:
            words = reduce_words(words, result.result())

    with timer("Printing results"):
        print("Total words: ", len(words))
        print("Total count for word : ", words[WORD])


if __name__ == "__main__":
    with timer("Total time"):
        asyncio.run(main())

