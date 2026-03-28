# RentElektro2

![Status](https://img.shields.io/badge/status-active-16a34a)
![Frontend](https://img.shields.io/badge/frontend-Vue%203%20%2B%20Vuetify-42b883)
![Backend](https://img.shields.io/badge/backend-FastAPI-009688)
![Database](https://img.shields.io/badge/database-PostgreSQL-336791)
![Migrations](https://img.shields.io/badge/migrations-Alembic-8b5cf6)
![Package Manager](https://img.shields.io/badge/backend%20deps-Poetry-3b82f6)
![Docker](https://img.shields.io/badge/dev-Docker%20Compose-2496ed)

NEW RentElektro is a marketplace-style web application for renting tools and managing offers, requests, payments, and listing lifecycle in one product flow. The project includes a FastAPI backend, a Vue 3 frontend, PostgreSQL, Redis, monitoring tooling, and a Docker-based local environment.

## What Is Included

- product-style frontend with homepage, tool catalog, tool profile, add-offer flow, user profile, and rentals center
- backend API for users, tools, rentals, account security, owner tool management, and notifications
- demo seed data with users, offers, reviews, and rental scenarios
- Docker setup for local development
- Alembic migrations for backend schema changes
- Prometheus / Grafana / NGINX / Redis / Directus infrastructure already wired into the repo

## Architecture

- `frontend_rentelektro`  
  Vue 3 + Vuetify frontend

- `backend_rentelektro`  
  FastAPI backend with Poetry, Alembic, and SQLAlchemy 2

- `nginx`  
  reverse proxy for local stack

- `fluentd`, `prometheus`, `grafana`  
  observability stack

## Quick Start

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd RentElektro2
```

### 2. Start the stack

```bash
docker compose up --build
```

For live development sync:

```bash
docker compose up --watch
```

## Main Services

- Frontend: `http://localhost:5173` or proxied through NGINX depending on your compose setup
- Backend API: `http://localhost:8000`
- Directus: `http://localhost:8055`
- Grafana: `http://localhost:3000`
- Prometheus: `http://localhost:9090`

## Backend Development

```bash
cd backend_rentelektro
poetry install
poetry run uvicorn app.main:app --reload
```

Useful commands:

```bash
poetry run alembic upgrade head
poetry run ruff check .
poetry run pytest
python3 -m app.scripts.seed_data
```

More backend details: [backend_rentelektro/README.backend.md](backend_rentelektro/README.backend.md)

## Frontend Development

```bash
cd frontend_rentelektro
npm install
npm run dev
```

Useful commands:

```bash
npm run typecheck
```

More frontend details: [frontend_rentelektro/README.frontend.md](frontend_rentelektro/README.frontend.md)

## Demo Data

The backend seed includes:

- multiple demo users
- categories and tool offers
- reviews
- rental requests in different states
- paid, active, archived, and rejected rental scenarios

Run:

```bash
cd backend_rentelektro
python3 -m app.scripts.seed_data
```

## Notes

- public tool list shows only active listings
- owners can manage their own listings directly from the tool profile
- rental center separates pending, current, archived, and owner inventory flows
- account deletion is handled as anonymization instead of hard delete

## Repository Status

The project has recently been updated with:

- SQLAlchemy 2 model style
- Poetry-based backend dependencies
- Alembic migrations
- backend linting via Ruff
- richer frontend UX and marketplace flows
