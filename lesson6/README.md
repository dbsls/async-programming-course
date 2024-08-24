# Lesson 6: Asynchronous Programming with CVE Files

## Overview
This lesson focuses on asynchronous programming in Python. The main objective is to scan a directory for CVE files, read and parse them, and store the data in a database using asynchronous I/O operations.

## Prerequisites
- Python 3.8+
- PostgreSQL database
- `pip` for package management

## Setup and Installation

1. **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd async-programming-course/lesson6
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Copy .env.template and change secrets.**

    ```sh
    cp app/.env.template app/.env
    ```

## Running the Script

1. **Run the main script:**
    ```sh
    python app/main.py <path-to-cves-directory>
    ```

    Replace `<path-to-cves-directory>` with the path to the directory containing your CVE files.

## Additional Information

- **Logging:** The script uses Python's logging module to log information and debug messages.
- **Error Handling:** The script includes error handling for file reading and JSON parsing errors.
- **Database:** The script uses SQLAlchemy for asynchronous database operations.

## Notes
- Ensure that your PostgreSQL database is running and accessible.
- The script processes files in chunks to optimize performance using multiple CPU cores.