# Omnihub

> Hexagonal, DDD-driven multi-tenant Agentic AI infrastructure orchestrator.

Omnihub is a FastAPI backend built around Hexagonal Architecture and Domain-Driven Design. It provides provider-agnostic authentication boundaries, identity persistence, organization/workspace context, and async PostgreSQL integration.

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
- [Available just Commands](#available-just-commands)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     HTTP Layer (FastAPI)               │
│              routes.py / schemas.py / middleware       │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│               Application Services                      │
│     auth/service.py · identity/service.py · orgs       │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│              Domain Layer (pure Python)                 │
│       entities.py · exceptions.py · ports (ABCs)        │
└──────────────┬─────────────────────────┬────────────────┘
               │                         │
┌──────────────▼──────────┐  ┌───────────▼──────────────┐
│   Auth Provider Adapter │  │      Postgres Adapter     │
│   (Supabase today)      │  │  asyncpg-backed adapters  │
└─────────────────────────┘  └──────────────────────────┘
```

- Domain logic does not depend on framework or provider SDKs.
- The auth guard depends on an injected auth provider port, not Supabase directly.
- Swapping identity providers requires adapter/wiring changes, not HTTP guard changes.

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| ASGI Server | Uvicorn |
| Auth Provider (current) | Supabase |
| Database | PostgreSQL + asyncpg |
| Cache / Queue | Redis |
| Migrations | dbmate |
| Package Manager | uv |
| Linting | Ruff |
| Type Checking | ty |
| Testing | pytest |

---

## Project Structure

```
src/omnihub/
├── cli.py                                  # App factory + uvicorn entrypoint
├── __main__.py                             # python -m omnihub entrypoint
├── common/
│   ├── db/pg_client.py                     # PgClient wrapper
│   ├── http/httpx_client.py                # Shared HTTPX client wrapper
│   ├── logging.py                          # Logging setup
│   └── time.py                             # Timestamp parser utility
├── config/
│   └── dotenv.py                           # .env loader
├── gateway/
│   ├── database.py                         # DB lifespan + middleware
│   ├── supabase.py                         # Supabase client factory
│   └── router.py                           # Central router aggregator
└── modules/
    ├── auth/
    │   ├── application/service.py
    │   ├── dependencies/
    │   │   ├── auth_guard.py               # get_current_user_token/get_authenticated_user_id
    │   │   └── auth_provider_dependency.py # provider + auth service factories
    │   ├── domain/
    │   ├── infrastructure/
    │   │   ├── http/
    │   │   └── supabase/
    │   └── ports/auth_provider_port.py
    ├── identity/
    │   ├── application/
    │   ├── domain/
    │   ├── infrastructure/
    │   │   ├── database/
    │   │   └── http/
    │   └── ports/
    └── organizations/
        ├── application/
        ├── dependencies/
        ├── domain/
        ├── infrastructure/
        │   ├── database/
        │   └── http/
        └── ports/
```

---

## Prerequisites

| Tool | Version |
|---|---|
| Python | >= 3.12 |
| uv | latest |
| Docker + Docker Compose | any recent |
| just | latest |
| dbmate | latest |
| Doppler CLI | latest |

Install just:

```bash
brew install just
```

Install dbmate:

```bash
brew install dbmate
```

Install Doppler CLI:

```bash
# macOS
brew install dopplerhq/cli/doppler

# Windows (scoop)
scoop bucket add doppler https://github.com/DopplerHQ/scoop-doppler.git
scoop install doppler

# Linux / other: see https://docs.doppler.com/docs/install-cli
```

---

## Environment Variables

Secrets for this project are managed with [Doppler](https://dashboard.doppler.com/workplace/89cc4a2706aa422b149b/projects/omnihub). Injection happens through two mechanisms depending on the process type:

- **Python processes** (dev server, worker, tests) — the [`doppler-env`](https://pypi.org/project/doppler-env/) package installs a `.pth` hook that shells out to `doppler secrets download` at interpreter startup and populates `os.environ`. It only runs when the `DOPPLER_ENV=1` env var is set, which the `justfile` exports for every recipe. If the Doppler CLI is missing, the hook logs a message and Python continues normally, falling through to the `.env` fallback below.
- **Non-Python tools** (dbmate) — wrapped explicitly with `doppler run --` in the `justfile`, since a `.pth` hook cannot reach a Go binary.

Application code just reads `os.environ` — no SDK integration in the codebase.

**Primary path — Doppler:**

```bash
doppler login              # one-time
doppler setup              # in the repo root; pick project `omnihub`, config `dev_personal`
just dev                   # secrets are injected automatically
```

`doppler setup` writes a `.doppler.yaml` in the repo root pointing at your chosen project/config. That file is per-developer (each person can pick their own config) and is git-ignored.

**Fallback — `.env` file:**

If you cannot install the Doppler CLI (e.g., quick offline experiments), copy `.env.example` to `.env` and fill in the values. The loader in `src/omnihub/config/dotenv.py` will pick it up. Doppler-injected values always take precedence over `.env`.

Required and optional keys are documented in `.env.example`. `SUPABASE_URL` and `SUPABASE_ANON_KEY` (or `SUPABASE_KEY`) are required for auth-enabled startup.

**CI / deploy:**

Set a Doppler service token as `DOPPLER_TOKEN` in your CI/deployment environment along with `DOPPLER_ENV=1`, `DOPPLER_PROJECT=omnihub`, and `DOPPLER_CONFIG=<your-config>`. `doppler-env` will hit the Doppler API directly (no CLI required). Non-Python tools still need the Doppler CLI installed and `doppler run --` wrapping.

**Running Python commands outside `just`:**

If you invoke Python directly (e.g., `uv run python -m omnihub` without going through `just`), set `DOPPLER_ENV=1` yourself — otherwise the doppler-env hook stays dormant and only the `.env` fallback applies.

---

## Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/howlerdevone/onmihub.git
cd omnihub

# 2. Install dependencies
uv sync

# 3. Configure environment (Doppler — preferred)
doppler login
doppler setup    # project: omnihub, config: dev_personal
# ...or, as a fallback: cp .env.example .env

# 4. Start infra (Postgres + Redis)
just docker-up

# 5. Run migrations
just db-up

# 6. Start the app
just dev
```

API: http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs

---

## Database Migrations

```bash
# Apply pending migrations
just db-up

# Create migration
just db-new create_some_table

# Roll back one migration
just db-rollback

# Status
just db-status
```

Migrations live in db/migrations and schema snapshot is in db/schema.sql.

---

## Running the Server

Development:

```bash
just dev
# equivalent (DOPPLER_ENV=1 triggers doppler-env to inject secrets at Python startup):
DOPPLER_ENV=1 OMNIHUB_RELOAD=true uv run python -m omnihub
```

Production example:

```bash
DOPPLER_ENV=1 DOPPLER_TOKEN=... DOPPLER_PROJECT=omnihub DOPPLER_CONFIG=prd \
  uv run uvicorn omnihub.cli:application --host 0.0.0.0 --port 8000 --workers 4
```

---

## Debugging

Use VS Code launch config with python -m omnihub, or run manually:

```bash
uv run python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m omnihub
```

---

## Development Workflow

```bash
just qa
just type-check
just test
just coverage
just pdb
```

---

## API Reference

### Auth — /v1/auth

| Method | Path | Description |
|---|---|---|
| GET | /v1/auth/health | Health check |
| POST | /v1/auth/register | Register user |
| POST | /v1/auth/login | Login user |

Register body:

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

Login body:

```json
{
  "email": "user@example.com",
  "password": "StrongPassword123!"
}
```

### Identity — /identity

| Method | Path | Description |
|---|---|---|
| GET | /identity/health | Health check |

### Organizations — /v1/organizations

Private endpoints using Bearer token.

| Method | Path | Description |
|---|---|---|
| POST | /v1/organizations | Create workspace for current user |
| GET | /v1/organizations/{workspace_id} | Get workspace context for current user |

Create workspace body:

```json
{
  "name": "Acme Workspace",
  "slug": "acme-workspace"
}
```

Common organization error codes:

| HTTP | Code | Meaning |
|---|---|---|
| 401 | AUTH_INVALID_TOKEN | Missing/invalid bearer token |
| 403 | ORG_ACCESS_DENIED | User has no access |
| 404 | ORG_NOT_FOUND | Workspace not found |
| 409 | ORG_ALREADY_EXISTS | Slug already exists |

---

## Available just Commands

```bash
just list
```

| Command | Description |
|---|---|
| just dev | Start dev server with reload |
| just docker-up | Start Docker services |
| just docker-down | Stop Docker services |
| just docker-destroy | Stop and remove volumes |
| just db-up | Apply migrations |
| just db-new NAME | Create migration |
| just db-rollback | Roll back last migration |
| just db-status | Show migration status |
| just qa | Format, lint, type-check, test |
| just test | Run pytest |
| just coverage | Run coverage flow |
| just type-check | Run ty |
| just build | Build package |
| just clean | Remove artifacts |
| just docs-serve | Serve docs |

---

## License

MIT — see LICENSE.
