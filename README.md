# Omnihub

> Hexagonal, DDD-driven multi-tenant Agentic AI infrastructure orchestrator.

Omnihub is a FastAPI backend built around **Hexagonal Architecture** and **Domain-Driven Design** principles. It provides a clean, provider-agnostic foundation for multi-tenant SaaS products with built-in auth, identity management, async database access, and a pluggable module system.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Getting Started](#getting-started)
- [Database Migrations](#database-migrations)
- [Running the Server](#running-the-server)
- [Debugging](#debugging)
- [Development Workflow](#development-workflow)
- [API Reference](#api-reference)
- [Available `just` Commands](#available-just-commands)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     HTTP Layer (FastAPI)                 │
│              routes.py / schemas.py / middleware         │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│               Application Services                      │
│         auth/service.py · identity/service.py           │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│              Domain Layer (pure Python)                 │
│       entities.py · exceptions.py · ports (ABCs)        │
└──────────────┬─────────────────────────┬────────────────┘
               │                         │
┌──────────────▼──────────┐  ┌───────────▼──────────────┐
│   Supabase Adapter      │  │    Postgres Adapter       │
│ auth_supabase_adapter   │  │  user_pg_adapter.py       │
└─────────────────────────┘  └──────────────────────────┘
```

- **Ports & Adapters (Hexagonal)** — domain logic never imports infrastructure.
- **DDD modules** — `auth` and `identity` are separate bounded contexts.
- **Provider-agnostic** — swap Supabase for Clerk/Auth0 by replacing the adapter only.

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| ASGI Server | Uvicorn (with uvloop) |
| Auth Provider | Supabase |
| Database | PostgreSQL 16 (asyncpg) |
| Cache / Queue | Redis 7 |
| Task Queue | Celery |
| Migrations | dbmate |
| Package Manager | uv |
| Linting | Ruff |
| Type Checking | ty (Pylance) |
| Testing | pytest / coverage |

---

## Project Structure

```
src/omnihub/
├── cli.py                        # App factory + uvicorn entrypoint
├── __main__.py                   # python -m omnihub entrypoint
├── config/
│   └── dotenv.py                 # Minimal .env loader
├── common/
│   ├── db/pg_client.py           # asyncpg PgClient wrapper
│   ├── http/httpx_client.py      # HTTPX client wrapper
│   ├── exceptions/http_error.py  # Shared HTTP exceptions
│   ├── logging.py                # Structured logging setup
│   └── time.py                   # Timestamp parsing utility
├── gateway/
│   ├── database.py               # DB lifespan + request middleware
│   ├── supabase.py               # Supabase client factory
│   └── router.py                 # Central router aggregator
└── modules/
    ├── auth/                     # Authentication bounded context
    │   ├── domain/               # Entities, exceptions
    │   ├── application/          # AuthApplicationService
    │   ├── ports/                # AuthProviderPort (ABC)
    │   ├── infrastructure/
    │   │   ├── http/             # Routes, schemas
    │   │   └── supabase/         # SupabaseAuthAdapter
    │   └── dependencies/         # FastAPI dependency factories
    └── identity/                 # Identity bounded context
        ├── domain/               # User entity, exceptions
        ├── application/          # IdentityApplicationService
        ├── ports/                # UserIdentityProviderPort (ABC)
        └── infrastructure/
            ├── database/         # UserPgIdentityAdapter
            └── http/             # Routes, schemas
```

---

## Prerequisites

| Tool | Version |
|---|---|
| Python | ≥ 3.12 |
| uv | latest |
| Docker + Docker Compose | any recent |
| just | latest |
| dbmate | latest |

Install `just`:
```bash
brew install just
```

Install `dbmate`:
```bash
brew install dbmate
```

---

## Environment Variables

Create a `.env` file at the project root:

```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key

# Database (optional, defaults to local Docker)
DATABASE_URL=postgres://omni_user:omni_password@localhost:5433/omnihub_dev

# Server (optional)
HOST=127.0.0.1
PORT=8000
OMNIHUB_RELOAD=true
```

> `SUPABASE_URL` and `SUPABASE_ANON_KEY` are required. The server will fail to start without them.

---

## Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/howlerdevone/onmihub.git
cd omnihub

# 2. Install dependencies
uv sync

# 3. Copy and fill environment variables
cp .env.example .env  # edit with your Supabase credentials

# 4. Start Docker services (Postgres + Redis)
just docker-up

# 5. Run database migrations
just db-up

# 6. Start the dev server
just dev
```

The API will be available at http://127.0.0.1:8000  
Interactive docs at http://127.0.0.1:8000/docs

---

## Database Migrations

Omnihub uses [dbmate](https://github.com/amacneil/dbmate) for schema migrations.

```bash
# Apply all pending migrations
just db-up

# Create a new migration
just db-new create_your_table_name

# Roll back the last migration
just db-rollback

# Show migration status
just db-status
```

Migration files live in `db/migrations/`. The current schema snapshot is in `db/schema.sql`.

---

## Running the Server

**Development (with auto-reload):**
```bash
just dev
# or
OMNIHUB_RELOAD=true uv run python -m omnihub
```

**Production:**
```bash
uv run uvicorn omnihub.cli:application --host 0.0.0.0 --port 8000 --workers 4
```

**Via entry point (after install):**
```bash
uv run omnihub
```

---

## Debugging

Open VS Code and press `F5` — the included launch config `Python: FastAPI` starts the server via `python -m omnihub` with debugpy attached and auto-reload enabled.

You can also attach to a running server manually:
```bash
uv run python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m omnihub
```

---

## Development Workflow

```bash
# Format + lint + type-check + test in one shot
just qa

# Type-check only
just type-check

# Run tests
just test

# Run tests with coverage
just coverage

# Run tests in debugger on failure
just pdb
```

---

## API Reference

### Auth — `/v1/auth`

| Method | Path | Description |
|---|---|---|
| `GET` | `/v1/auth/health` | Health check |
| `POST` | `/v1/auth/register` | Register new user |
| `POST` | `/v1/auth/login` | Login existing user |

**Register** `POST /v1/auth/register`
```json
{
  "email": "user@example.com",
  "password": "StrongPassword123!",
  "display_name": "Jane Doe",
  "timezone": "America/New_York",
  "birthdate": "1990-05-15",
  "preferred_language": "en"
}
```

**Login** `POST /v1/auth/login`
```json
{
  "email": "user@example.com",
  "password": "StrongPassword123!"
}
```

**Error Codes**

| HTTP | Code | Meaning |
|---|---|---|
| 401 | `AUTH_INVALID_CREDENTIALS` | Wrong email or password |
| 409 | `AUTH_USER_ALREADY_EXISTS` | Email already registered |
| 400 | `AUTH_ERROR` | Auth request could not be processed |
| 500 | `SYSTEM_ERROR` | Unexpected server error |

### Identity — `/identity`

| Method | Path | Description |
|---|---|---|
| `GET` | `/identity/health` | Health check |

---

## Available `just` Commands

```bash
just list
```

| Command | Description |
|---|---|
| `just dev` | Start dev server with auto-reload |
| `just docker-up` | Start Postgres + Redis in background |
| `just docker-down` | Stop Docker services |
| `just docker-destroy` | Stop and remove volumes |
| `just db-up` | Apply all migrations |
| `just db-new NAME` | Create a new migration |
| `just db-rollback` | Roll back last migration |
| `just db-status` | Show migration status |
| `just qa` | Format + lint + type-check + test |
| `just test` | Run pytest |
| `just coverage` | Run tests with coverage report |
| `just type-check` | Run ty type checker |
| `just build` | Build distribution packages |
| `just clean` | Remove build/test artifacts |
| `just docs-serve` | Serve docs locally |

---

## License

MIT — see [LICENSE](LICENSE).
