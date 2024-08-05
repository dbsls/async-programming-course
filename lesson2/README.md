# README

## Overview

The `url_fetcher.py` script is designed to fetch content from a list of URLs provided in a file and save the 
fetched content to individual HTML files. The script uses asynchronous programming with the `asyncio` and `aiohttp` 
libraries to perform the fetching and saving operations concurrently.

## Requirements

- Python 3.7+
- `aiohttp` library
- `aiofiles` library

## Installation

1. Clone the repository or download the script.
2. Install the required libraries using pip:

    ```sh
    pip install aiohttp aiofiles
    ```

## Usage

To run the script, use the following command:

```sh
python url_fetcher.py <path_to_urls_file>
```

### Arguments

- `<path_to_urls_file>`: Path to the file containing the list of URLs to fetch.

### Example

```sh
python url_fetcher.py homework/urls.txt
```

## Script Details

### Functions

- `ensure_dir_exists(f_name: str) -> None`: Ensures the directory for saving results exists.
- `get_new_file_name(url: str) -> str`: Generates a new file name based on the URL.
- `save_to_file(url: str, data: str) -> None`: Saves the fetched data to a file.
- `process_results(results: tuple[Any]) -> None`: Processes the fetched results and saves them to files.
- `fetch_url(url: str) -> str`: Fetches the content of a URL.
- `run_fetching(url: str) -> tuple`: Manages the fetching process with timeout handling.
- `create_tasks(file: str) -> list`: Creates tasks for fetching URLs from the provided file.
- `main(file: str) -> None`: Main function to run the script.

### Logging

The script uses the `logging` module to log information, warnings, and errors. Logs are printed to the console.

### Timeouts

- `FETCH_TIMEOUT`: Timeout for fetching a URL (default: 3 seconds).
- `SAVE_TO_FILE_TIMEOUT`: Timeout for saving data to a file (default: 0.2 seconds).

## Error Handling

- The script checks if the URLs file exists before reading.
- Handles `TimeoutError` and `ClientConnectionError` during fetching.
- Handles `TimeoutError` and `FileNotFoundError` during saving.

## Directory Structure

- `fetching_results/`: Directory where the fetched HTML files are saved.

## License

This project is licensed under the MIT License.