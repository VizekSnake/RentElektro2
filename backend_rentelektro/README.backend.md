
### Backend README

# RentElektro Backend

This is the backend service for the RentElektro project, built with FastAPI.

## Features

- RESTful API for managing users, tools, and rentals
- JWT-based authentication
- Integration with PostgreSQL
- Real-time monitoring with Prometheus

## Technology Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
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

Local Poetry commands load `envs/config.dev.env` and `envs/postgres.dev.env` automatically. The committed dev database config points to `127.0.0.1:5432`, so commands started on your host machine can talk to the PostgreSQL container exposed by Docker. Docker Compose overrides `POSTGRES_HOST=postgres` inside containers. Use `APP_DEBUG=true|false` in project env files instead of a generic `DEBUG` variable, which often collides with shell or IDE defaults.

Application settings follow the FastAPI pattern from the official docs: `Settings` lives in `app/core/config.py` and `get_settings()` caches a single instance with `@lru_cache`.

Run tests:

```bash
poetry run pytest
```

### Seed development data

After PostgreSQL is running and the schema has been created with Alembic, you can fill the database with a repeatable starter dataset:

```bash
docker compose up -d postgres
poetry run alembic upgrade head
poetry run python -m app.scripts.seed_data
```

The seed is idempotent for the prepared records, so re-running it should not duplicate the sample users, categories, tools, rentals, or reviews. It no longer creates tables on its own.

### Alembic migrations

The backend now includes a basic Alembic setup in `backend_rentelektro/migrations`.

To run the current migration chain:

```bash
cd backend_rentelektro
poetry run alembic upgrade head
```

Alembic is the only supported migration path for schema changes. Do not modify tables with ad hoc SQL scripts outside migration files.

Environment variables for PostgreSQL are read in `alembic/env.py`, so use the same `.env` / container environment as the application.

If you have an old local database created before Alembic became the only schema path, recreate it or stamp it manually before using migrations:

```bash
poetry run alembic stamp head
```

Use `stamp head` only when the existing schema already matches the current models.

### Ruff linting

Backend uses `ruff` configuration from `backend_rentelektro/pyproject.toml`.

Format code:

```bash
cd backend_rentelektro
poetry run ruff format .
```

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

### Pre-commit hooks

Backend uses `pre-commit` hooks for automated checks before commit and push.

Install hooks:

```bash
poetry -C backend_rentelektro run pre-commit install --hook-type pre-commit --hook-type pre-push
```

Run them manually on the whole repo:

```bash
poetry -C backend_rentelektro run pre-commit run --all-files
```

Configured checks:

- `pre-commit`: `ruff format --check`, `ruff check`
- `pre-push`: `pytest`
