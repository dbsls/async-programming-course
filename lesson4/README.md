# Philosophers Dinner Problem

## Overview

This project demonstrates the solution to the classic Dining Philosophers problem using Python's `asyncio` library.
The solution employs semaphores to prevent deadlock and ensure that philosophers can eat and think concurrently 
without conflicts.

## Project Structure

```
lesson4/
└── philosophers.py
```

### File

- `philosophers.py`: Contains the implementation of the Dining Philosophers problem 
- using `asyncio`, `asyncio.Lock`, `asyncio.Semaphore`

## Getting Started

### Prerequisites

- Python 3.7 or higher
- `asyncio` library (included in the Python standard library)

### Running the Script

1. Navigate to the directory containing `philosophers.py`.
2. Run the script:
   ```sh
   python philosophers.py
   ```

## Detailed Explanation

### `philosophers.py`

This file contains the implementation of the Dining Philosophers problem. It includes the following components:

- **Philosopher Class**: Represents a philosopher who alternates between thinking and eating. 
Each philosopher tries to pick up two forks (represented by `asyncio.Lock`) and uses a semaphore to limit 
the number of philosophers attempting to eat simultaneously.
- **Main Function**: Sets up the philosophers, forks, and semaphore, and starts the dining process.

### Logging

Logging is configured to provide detailed information about the philosophers' actions. The log level and format are set at the beginning of the file.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.