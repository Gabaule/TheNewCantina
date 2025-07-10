# The New Cantina

A web application for ordering meals at a university cafeteria. It includes role-based access for students, staff, and administrators, balance management, and menu viewing.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Project Scripts](#project-scripts)
- [Default Credentials](#default-credentials)
- [Project Structure](#project-structure)

## Prerequisites

- Docker
- Docker Compose
- Python 3.9+ (for local script execution)
- Git

## Setup and Installation

The project is designed to be run using Docker Compose, which handles the setup of the application, database, and all dependencies.

1.  **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Build and run the services:**
    This command will build the Flask application image, start the PostgreSQL database, and run the application in the background. The first time the application starts, the database schema will be created and populated with seed data.
    ```sh
    docker compose -f docker/docker-compose.yml up --build -d
    ```

## Running the Application

Once the Docker containers are running, the application will be available at:

-   **Web Application**: [http://localhost:8081](http://localhost:8081)
-   **pgAdmin (Database Admin Tool)**: [http://localhost:5050](http://localhost:5050)
    -   pgAdmin Email: `admin@example.com`
    -   pgAdmin Password: `password`

To stop the services and remove the associated volumes (including the database data), run:
```sh
docker compose -f docker/docker-compose.yml down -v
```

## Running Tests

Tests are written using `pytest` and can be run in several ways. The recommended method is to execute them within the Docker container to ensure a consistent environment.

### Method 1: Run tests inside the Docker container (Recommended)

This command executes the entire test suite directly inside the running `python-app` container.

```sh
docker compose -f docker/docker-compose.yml exec python-app pytest -v
```

This will run all unit, API, and end-to-end tests located in the `tests/` directory.

### Method 2: Use the Report Generator Script

The project includes a script that runs tests and generates a comprehensive report. This is ideal for formal test execution.

1.  **Install dependencies for the script:**
    ```sh
    pip install openpyxl
    ```

2.  **Run tests and generate reports:**
    -   To run tests :
        ```sh
        python report_generator.py
        ```
    This script will execute `pytest`, generate `tests_results.xml`, and create a `Complete_Testing_Report.md`.

### Method 3: Run tests locally (Advanced)

For local development, you can run tests directly on your machine. This requires setting up a Python virtual environment and installing all dependencies.

1.  **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2.  **Install project dependencies:**
    *(Assuming a requirements.txt file exists or can be generated from project metadata)*
    ```sh
    pip install -r requirements.txt
    ```

3.  **Run pytest:**
    ```sh
    pytest
    ```

## Project Scripts

### Test Report Generator

-   **File**: `report_generator.py`
-   **Purpose**: Automates test execution and generates formal test reports in Markdown and PDF format. It combines results from automated `pytest` runs and manual tests documented in an Excel file.
-   **Usage**:
    ```sh
    python report_generator.py --output-pdf TestReport.pdf

    # Use existing XML results to generate a report without re-running tests
    python report_generator.py --no-run-tests
    ```
-   **Arguments**:
    -   `--no-run-tests`: Skip test execution and use an existing XML file.
    -   `--xml-file`: Path to the JUnit XML results file.
    -   `--manual-tests-excel`: Path to the Excel file with manual test cases.
    -   `--output-md`: Path for the output Markdown report.
    -   `--output-pdf`: Path for the output PDF report (requires Pandoc and a LaTeX distribution).

## Default Credentials

The database is seeded with the following user accounts for demonstration and testing:

| Role      | Email                   | Password   |
| :-------- | :---------------------- | :--------- |
| **Admin** | `admin@example.com`     | `password` |
| Student   | `student1@example.com`  | `pass123`  |
| Student   | `jakub.novak@example.com`| `pass123`  |
| Staff     | `faculty1@example.com`  | `pass123`  |

## Project Structure

A brief overview of the key directories:

```
.
├── app/                  # Main Flask application source code
│   ├── controller/       # Flask controllers (routes) and auth logic
│   ├── models/           # SQLAlchemy database models
│   ├── templates/        # Jinja2 HTML templates
│   ├── db_seeder.py      # Script to populate the database with initial data
│   └── main.py           # Application entry point
├── db-init/              # SQL scripts for database initialization
│   └── init.sql
├── docker/               # Docker configuration files
│   ├── Dockerfile
│   └── docker-compose.yml
├── tests/                # All tests for the project
│   └── test-python/      # Pytest tests
│       ├── controller/   # API and controller tests
│       ├── models/       # Unit tests for SQLAlchemy models
│       └── selenium-e2e/ # Selenium end-to-end tests
└── report_generator.py     # Script to run tests and generate reports
```