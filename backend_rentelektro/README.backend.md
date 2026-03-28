
### Backend README

# RentElektro Backend

This is the backend service for the RentElektro project, built with FastAPI.

## Features

- RESTful API for managing users, tools, and rentals
- JWT-based authentication
- Integration with PostgreSQL, MongoDB, and Redis
- Real-time monitoring with Prometheus

## Technology Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL, MongoDB
- **Cache:** Redis
- **Monitoring:** Prometheus
- **Containerization:** Docker

## Prerequisites

- Docker and Docker Compose

## Getting Started

### Navigate to the backend directory

```bash
cd backend_rentelektro
```

### Install dependencies with Poetry

The backend now uses Poetry instead of `requirements.txt`.

Install locally:

```bash
poetry install
```

Run the app locally:

```bash
poetry run uvicorn app.main:app --reload
```

Run tests:

```bash
poetry run pytest
```

### Seed development data

After PostgreSQL is running and environment variables are loaded, you can fill the database with a repeatable starter dataset:

```bash
python3 -m app.scripts.seed_data
```

The seed is idempotent for the prepared records, so re-running it should not duplicate the sample users, categories, tools, rentals, or reviews.

### Upgrade rentals schema

If you already have an existing database and want to use the newer rental payment / pickup / return fields, run:

```bash
python3 -m app.scripts.upgrade_rentals_schema
```

### Alembic migrations

The backend now includes a basic Alembic setup in `backend_rentelektro/alembic`.

To run the current migration chain:

```bash
cd backend_rentelektro
poetry run alembic upgrade head
```

Environment variables for PostgreSQL are read in `alembic/env.py`, so use the same `.env` / container environment as the application.

By default the app still auto-runs `Base.metadata.create_all()` on startup. If you want to rely only on migrations, set:

```bash
AUTO_CREATE_SCHEMA=false
```

### Ruff linting

Backend uses `ruff` configuration from `backend_rentelektro/pyproject.toml`.

Run lint:

```bash
cd backend_rentelektro
poetry run ruff check .
```

Auto-fix import ordering and basic issues:

```bash
cd backend_rentelektro
poetry run ruff check . --fix
```
