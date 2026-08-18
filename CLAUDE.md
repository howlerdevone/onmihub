# Omnihub Project Guide

## Project Overview

Omnihub is a FastAPI-based Python boilerplate for building scalable backend services with proper architecture patterns (clean architecture with domain-driven design).

- **Type:** Python Backend (FastAPI)
- **Python:** ≥ 3.12
- **Package Manager:** uv
- **Database:** PostgreSQL (async with asyncpg)
- **Authentication:** Supabase
- **Task Queue:** Celery + Redis
- **API Framework:** FastAPI

## Tech Stack

- **Framework:** FastAPI 0.115+
- **Async ORM:** SQLAlchemy 2.0+
- **Database Driver:** asyncpg
- **Validation:** Pydantic 2.x
- **Code Quality:**
  - Linting/Formatting: Ruff
  - Type Checking: ty (Pyright-based)
  - Testing: pytest + coverage (50% minimum)
  - Pre-commit hooks: for local validation

## Directory Structure

```
src/omnihub/
├── common/              # Shared utilities & base models
│   ├── base_models.py   # CustomBaseModel (camelCase serialization)
│   ├── db/              # Database clients
│   ├── http/            # HTTP utilities
│   └── exceptions/      # Custom exceptions
├── config/              # Configuration & settings
├── modules/
│   ├── auth/            # Authentication module
│   │   ├── domain/      # Business logic & entities
│   │   ├── application/ # Use cases & services
│   │   ├── infrastructure/
│   │   │   ├── database/# Database adapters
│   │   │   └── http/    # API routes & schemas
│   │   └── dependencies/
│   ├── identity/        # User management
│   ├── organizations/   # Workspace/org management
│   └── [other modules]
├── cli.py               # CLI entrypoint
└── main.py              # FastAPI app entrypoint
```

## API Response Format

All API responses are automatically converted to **camelCase** in responses while code uses **snake_case**. This is handled by `CustomBaseModel` in `common/base_models.py`.

**Example:**
```python
# Code
class AuthUserResponse(CustomBaseModel):
  firstname: str
  preferred_language: str


# Response JSON
{"firstname": "John", "preferredLanguage": "es"}
```

## Database

- **Tool:** PostgreSQL with dbmate migrations
- **Migrations:** `db/migrations/` (auto-timestamped)
- **Connection:** Async via asyncpg through `PgClient`

### Running Migrations

```bash
just db-up       # Apply pending migrations
just db-status   # Check migration status
just db-rollback # Rollback last migration
just db-new NAME # Create new migration
```

## Development

### Setup

```bash
# Install dependencies
uv sync

# Start Docker services
just docker-up

# Apply migrations
just db-up

# Start dev server
just dev
```

### Common Commands

```bash
just qa              # Format + Lint + Type-check + Test (all in one)
just test            # Run tests
just type-check      # Run type checker
just coverage        # Generate coverage report
just docker-up       # Start Docker services
just docker-down     # Stop Docker services
just docker-destroy  # Full cleanup (removes data)
```

### Pre-commit Hooks

Install and enable pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files  # Test all files
```

Hooks will auto-run on commit and check:
- Format (Ruff)
- Linting (Ruff)
- Type checking (ty)
- Trailing whitespace
- Large files
- Detect private keys

## Code Quality Standards

### Formatting
- **Formatter:** Ruff (not Black)
- **Indent:** 2 spaces
- **Line Length:** 120 characters
- **Command:** `uv run ruff format .`

### Linting
- **Tool:** Ruff
- **Rules:** E, W, F, I, B, UP (see pyproject.toml)
- **Command:** `uv run ruff check . --fix`

### Type Checking
- **Tool:** ty (Pyright-based)
- **Level:** Strict (all errors reported)
- **Command:** `uv run ty check .`

### Testing
- **Framework:** pytest
- **Coverage Minimum:** 50%
- **Command:** `uv run pytest`
- **Coverage:** `uv run coverage report`

## Architecture Notes

### Modules Pattern
Each module follows clean architecture:
- **Domain:** Entities, ports (interfaces), business logic
- **Application:** Services, use cases
- **Infrastructure:** Database adapters, HTTP routes, external integrations
- **Dependencies:** Dependency injection setup

### Example: Auth Module
```
modules/auth/
├── domain/
│   ├── entities.py
│   └── exceptions.py
├── application/
│   └── service.py          # Business logic
├── infrastructure/
│   ├── database/           # Data access
│   ├── http/               # API routes & schemas
│   └── [other infra]
└── dependencies/           # DI setup
```

### Custom Base Model
All response models should extend `CustomBaseModel` (not `BaseModel`):
- Auto-converts snake_case fields to camelCase in JSON responses
- Accepts both snake_case and camelCase in request bodies
- See: `src/omnihub/common/base_models.py`

## CI/CD

### GitHub Actions

Runs on every PR and push to main:
1. **Lint** - Ruff format + check
2. **Type Check** - ty checker
3. **Test** - pytest on Python 3.12, 3.13, 3.14
4. **Coverage** - Reports coverage metrics

## Environment Variables

See `.env.example` for all available variables. Required for local dev:

```bash
cp .env.example .env
# Edit .env with your local values
```

Key variables:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection
- `SUPABASE_URL`, `SUPABASE_KEY` - Authentication

## Common Issues

### Pre-commit hook issues
If pre-commit fails:
```bash
pre-commit run --all-files    # Debug all files
pre-commit clean              # Clear cache
```

### Type errors after refactoring
Run full type check:
```bash
uv run ty check --output-format=concise .
```

### Database connection errors
Check Docker is running:
```bash
docker ps | grep omnihub
just db-status  # Verify migrations
```

## Useful Resources

- **FastAPI:** https://fastapi.tiangolo.com
- **SQLAlchemy Async:** https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- **Pydantic:** https://docs.pydantic.dev/2.0/
- **Ruff:** https://docs.astral.sh/ruff/
- **py (Type Checker):** https://github.com/inferential/pyright

## When Adding Claude Code

For best results in future Claude Code sessions:
1. Keep this CLAUDE.md updated with new modules/patterns
2. Use consistent architecture across modules
3. Test all changes with `just qa` before committing
4. Write clear commit messages following conventional commits

---

**Last Updated:** 2026-08-17
