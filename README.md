# Python Backend with FastAPI

This project is a comprehensive backend service built with Python and FastAPI. It is a secure, scalable, and well-tested application that implements a full-featured RESTful API handling user authentication, data persistence, and business logic, following industry best practices.

## What I've Learned & Implemented

This project demonstrates my proficiency in the following areas:

- **Asynchronous APIs**: Developed a high-performance API with **FastAPI** using `async/await`.
- **Database & ORM**: Managed database interactions and schema design with **SQLAlchemy**.
- **Database Migrations**: Handled schema versioning using **Alembic**.
- **Data Validation**: Ensured data integrity with **Pydantic** schemas.
- **Authentication**: Implemented secure JWT-based user authentication with password hashing.
- **Dependency Injection**: Used FastAPI's dependency injection for cleaner, more testable code.
- **Code Structure**: Organized the project into a scalable and maintainable modular layout.
- **Testing**: Wrote comprehensive unit and integration tests with **Pytest**.
- **Configuration**: Managed application settings and secrets via environment variables.

## Built With

This project is built with these amazing technologies:

- [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance) web framework for building APIs.
- [SQLAlchemy](https://www.sqlalchemy.org/): A powerful SQL toolkit and Object-Relational Mapper (ORM).
- [Alembic](https://alembic.sqlalchemy.org/): A lightweight database migration tool for SQLAlchemy.
- [Pydantic](https://pydantic-docs.helpmanual.io/): Data validation and settings management using Python type annotations.
- [Pytest](https://docs.pytest.org/): A framework that makes it easy to write small, readable tests.

## Getting Started

Follow these simple steps to get a local copy up and running.

### Prerequisites

Make sure you have Python 3.8 or higher installed on your system.

### Installation

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/kayesFerdous/fastapi-auth-service-.git
    cd fastapi-auth-service-
    ```

2.  **Create and activate a virtual environment:**

    ```sh
    # For Linux/macOS
    python3 -m venv .venv
    source .venv/bin/activate

    # For Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**

    Create a file named `.env` in the project root and add the following variables. This file stores your secret keys and database settings.

    ```env
    # Example .env file
    DATABASE_URL="postgresql://user:password@host:port/database_name"
    SECRET_KEY="your_very_secret_key"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

5.  **Run database migrations:**

    This command will create all the necessary tables in your database based on the models defined in the code.

    ```sh
    alembic upgrade head
    ```

## How to Run

To start the application, run the following command. The server will automatically reload when you make changes to the code.

```sh
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:3000`.

## Running Tests

To make sure everything is working as expected, you can run the test suite:

```sh
pytest
```

## Project Layout

Here is a brief overview of the project's structure:

```
├───crud/         # Functions to Create, Read, Update, Delete data from the database.
├───database.py   # Database connection and session setup.
├───main.py       # The main entry point of the application.
├───models/       # SQLAlchemy database models (the table structures).
├───routes/       # All the API endpoint definitions (e.g., /users, /tasks).
├───schemas/      # Pydantic models for data validation and serialization.
├───security/     # Code related to authentication and authorization.
└───tests/        # All the tests for the application.
```
