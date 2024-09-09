### README

# Final Project: CVE Change Checker and API

## Overview

This project consists of two main components:
1. **CVE Change Checker**: A FastAPI application that periodically downloads and scans CVE data.
2. **CVE API**: A FastAPI application that provides endpoints to interact with CVE data stored in a PostgreSQL database.

## Prerequisites

- Python 3.8+
- Docker
- PostgreSQL
- Node.js and npm (for any frontend components)

## Setup

### 1. Clone the Repository

```sh
git clone <repository_url>
cd async-programming-course/final_project
```



### 2. Configure Environment Variables

Create a `.env` file in the `final_project` directory according to `.env.example`.

### 3. Run docker containers

```sh
docker compose up
```

## Usage

### CVE Change Checker Endpoints

- **GET `/`**: Buttons to trigger downloading for all cves or only latest changes.
- **GET `/download-cve`**: Initiates a scan of the CVE path.
- **GET `/download-cve-last-changes`**: Downloads the latest changes in CVE data.

### CVE API Endpoints

- **GET `/items/{item_id}`**: Retrieves a CVE item by ID.
- **GET `/items/search/`**: Searches for CVE items by date range or description.
- **POST `/items/`**: Adds a new CVE item or updates an existing one.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.