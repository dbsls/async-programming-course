# Lesson 8: Async Programming with FastAPI

## Description
This project demonstrates asynchronous programming using FastAPI, SQLAlchemy, and PostgreSQL. It includes endpoints for managing CVE (Common Vulnerabilities and Exposures) data.

## Installation

1. **Clone the repository**:
    ```sh
    git clone <repository_url>
    cd async-programming-course/lesson8
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the FastAPI application**:
    ```sh
    uvicorn app.main:app --reload
    ```

2. **Access the API documentation**:
    - Open your browser and go to `http://127.0.0.1:8000/docs` for the Swagger UI or `http://127.0.0.1:8000/redoc` for ReDoc.

## Endpoints

- **GET /**: Welcome message
- **GET /items/**: Retrieve all CVE items
- **GET /items/{item_id}**: Retrieve a specific CVE item by ID
- **POST /items/**: Create a new CVE item

## Database

1. **Setup the database**:
    - Ensure PostgreSQL is installed and running.
    - Create a database for the project.

2. **Configure the database connection**:
    - Update the `config.py` file with your PostgreSQL DSN.

3. **Run database migrations**:
    ```sh
    alembic upgrade head
    ```

## License
This project is licensed under the MIT License.