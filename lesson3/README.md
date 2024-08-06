# Lesson 3: Asynchronous Programming with `asyncio`

## Overview

This lesson covers the basics of creating asynchronous servers and clients, handling streaming data.

## Project Structure

```
lesson3/
├── client.py
├── server_v1.py
├── server_v2.py
└── thermometer.py
```

### Files

- `client.py`: Contains the client implementation that connects to the server and requests temperature data.
- `server_v1.py`: Implements a server using `asyncio` streaming protocols to handle client connections and stream temperature data.
- `server_v2.py`: Implements a server using `asyncio.Protocol` to handle client connections and stream temperature data.
- `thermometer.py`: Contains the `Thermometer` class, which simulates temperature measurements.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- `asyncio` library (included in the Python standard library)

### Running the Server

1. **Server Version 1**:
   ```sh
   python server_v1.py
   ```

2. **Server Version 2**:
   ```sh
   python server_v2.py
   ```

### Running the Client

1. Ensure the server is running.
2. Run the client:
   ```sh
   python client.py
   ```

## Detailed Explanation

### `thermometer.py`

This file contains the `Thermometer` class, which simulates temperature measurements. It uses a singleton pattern to ensure only one instance of the thermometer exists.

### `server_v1.py`

This server uses `asyncio` streaming protocols to handle client connections. It reads data from the client, streams temperature data, and handles connection resets.

### `server_v2.py`

This server uses `asyncio.Protocol` to handle client connections. It streams temperature data to the client and logs connection events.

### `client.py`

This client connects to the server, sends a request for temperature data, and logs the received data.

## Logging

Logging is configured in each file to provide detailed information about the server and client operations. The log level and format are set at the beginning of each file.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.