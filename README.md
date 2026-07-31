# 📈 Crypto Index Price API — FastAPI + Celery + PostgreSQL

A backend service that periodically fetches BTC and ETH index prices from
Deribit, stores them in PostgreSQL, and provides a public API for analysis.

Features:
- Scheduled price fetching every minute (Celery Beat)
- Historical price storage
- REST API for querying prices

---

## 🚀 Features

- ⏱️ Automated collection of BTC_USD and ETH_USD every minute
- 🗄 Historical price storage in PostgreSQL
- 📊 API for:
  - last price
  - all prices (paginated)
  - prices filtered by date range
- 🐇 Celery + RabbitMQ for background tasks
- 🐳 Docker + docker-compose
- ⚡ FastAPI + async SQLAlchemy

---

## 🏗 Architecture

The application follows **Clean Architecture** with clear separation of concerns:

```
src/
├── application/ # Service layer (business logic)
│ ├── services/
│ └── constants.py
├── domain/ # Entities and repository interfaces
│ ├── entities.py
│ └── repositories.py
├── infrastructure/ # ORM models, repository implementations, Unit of Work
│ ├── models/
│ ├── repositories/
│ └── unit_of_work.py
├── presentation/ # FastAPI routers, Pydantic schemas, dependencies
│ ├── api/
│ ├── schemas/
│ └── dependencies.py
├── config/ # Pydantic settings
├── db/ # Database engine and session factory
├── clients/ # External API clients (Deribit)
├── tasks/ # Celery tasks
├── app.py # Application entry point
└── celery_app.py # Celery configuration
```

---

## ⚙️ Stack

- FastAPI
- Celery 5
- RabbitMQ
- PostgreSQL
- aiohttp
- SQLAlchemy 2 (async)
- Pydantic + pydantic-settings
- Docker + docker-compose
- Poetry (dependency management)
- pytest (unit, integration, e2e)
- Ruff / MyPy / pre-commit

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/Eygenio/Deribit_crypto_exchange_client
```

## 2. Create a `.env` file (or copy from the provided template):

```
APP__HOST=0.0.0.0
APP__PORT=8000

DB__NAME=database
DB__USER=postgres
DB__PASSWORD=postgres
DB__HOST=db
DB__PORT=5432
DB__DRIVER_NAME=postgresql+asyncpg

BROKER__URL=amqp://guest:guest@rabbitmq:5672//
BROKER__RESULT_BACKEND=rpc://
```

## 3. 🐳 Build & run with Docker

```bash
docker-compose build
docker-compose up -d
```

The service will be available at `http://localhost:8000`.
Interactive API docs: `http://localhost:8000/docs`.

## 📡 API

### Get last price
```bash
GET /api/price/last?ticker=btc_usd
```

### Get all prices (paginated)
```bash
GET /api/prices?ticker=btc_usd&page=1
```
### Get prices by date range
```bash
GET /api/price/by-date?ticker=btc_usd&from_ts=1700000000&to_ts=1700100000&page=1
```

---

## 🧠 Design decisions

* **Celery** — reliably runs scheduled tasks and scales data collection.
* **aiohttp** — async HTTP client that doesn't block the FastAPI/Celery event loop.
* **Repository Pattern + Unit of Work** — isolates business logic from SQL, simplifies testing and DB changes.
* **UNIX timestamp** — easy to compare, filter, and index.
* **Pagination** — prevents returning thousands of rows at once.

---

## 🧪 Testing

```bash
docker-compose exec app pytest -v
```
Tests are organized into:
* **unit** — services with mocked UoW
* **integration** — API + real DB (SQLite in-memory)
* **e2e** — full flow from API to DB
*
---

## 🧹 Code Quality

All code quality tools are configured in `pyproject.toml` and `.pre-commit-config.yaml`.

```bash
# Formatting and linting
ruff check . --fix
ruff format .

# Type checking
mypy src
```

Pre-commit hooks run automatically on `git commit`.

---

## 🔐 Security

* No authentication required (public API)
* PostgreSQL isolated within Docker network
* Environment variables for all sensitive configuration

---
