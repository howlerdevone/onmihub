# Contributing to Omnihub

Contributions are welcome! Thank you for helping improve Omnihub. This guide will help you get started.

## Prerequisites

- Python ≥ 3.12
- Docker & Docker Compose
- uv (Astral's Python package manager)
- Git

## Quick Start

1. **Clone & Setup**
   ```bash
   git clone https://github.com/howlerdevone/omnihub.git
   cd omnihub
   uv sync
   ```

2. **Install Git Hooks** (Important!)
   ```bash
   just pre-commit-install
   ```
   This ensures code quality standards before commits.

3. **Start Docker**
   ```bash
   just docker-up
   just db-up
   ```

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/howlerdevone/omnihub/issues.

Include:
- Operating system and version
- Steps to reproduce
- Expected vs actual behavior

### Fix Bugs

Look for issues tagged `bug` + `help wanted` at https://github.com/howlerdevone/omnihub/issues.

### Implement Features

Look for issues tagged `enhancement` + `help wanted`.

### Write Documentation

Documentation improvements are always welcome:
- Update [CLAUDE.md](CLAUDE.md) with new patterns
- Add docstrings to code
- Improve README or contributing guides

Preview docs locally:
```bash
just docs-serve
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feat/my-feature  # or fix/bug-name
```

### 2. Make Your Changes

Follow code standards:
- **Code Style:** 2 spaces, max 120 line length
- **Type Hints:** All functions must have type hints
- **Testing:** Write tests for new features
- **Imports:** Alphabetically sorted (enforced by Ruff)

### 3. Run Quality Checks

Before committing, run all checks:

```bash
just qa
```

This runs:
- ✓ Code formatting (Ruff)
- ✓ Linting (Ruff)
- ✓ Type checking (ty)
- ✓ Tests (pytest)

Or individually:
```bash
uv run ruff format .        # Format code
uv run ruff check . --fix   # Lint & fix
uv run ty check .           # Type check
just test                   # Run tests
```

### 4. Commit with Conventional Commits

Use this format:
```
<type>(<scope>): <subject>
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `refactor:` - Code refactoring
- `perf:` - Performance improvement
- `test:` - Adding/updating tests
- `docs:` - Documentation
- `chore:` - Dependencies, maintenance

**Examples:**
```bash
git commit -m "feat(auth): add two-factor authentication"
git commit -m "fix(db): handle null timezone values"
git commit -m "refactor(models): simplify user entity"
```

### 5. Push & Open PR

```bash
git push origin feat/my-feature
```

Then open a Pull Request on GitHub with:
- Clear title (follows Conventional Commits)
- Description of changes
- Link to related issues
- Testing notes

## Code Standards

### Formatting

Code formatting is automatic with Ruff:
```bash
uv run ruff format .
```

- **Indent:** 2 spaces (not tabs)
- **Line Length:** 120 characters
- **Tool:** Ruff (like Prettier for Python)

### Type Checking

Strict typing is required:
```bash
uv run ty check .
```

All functions must have type hints:
```python
async def create_user(email: str, password: str) -> User:
    """Create a new user."""
    ...
```

### API Responses

Always use `CustomBaseModel` for responses:
```python
from omnihub.common import CustomBaseModel

class UserResponse(CustomBaseModel):
    first_name: str      # Code uses snake_case
    preferred_language: str

# Response JSON automatically converts to camelCase:
# { "firstName": "...", "preferredLanguage": "..." }
```

## Testing

Write tests for all new features:

```bash
# Run all tests
just test

# Run specific test
uv run pytest tests/auth/test_login.py

# Run with coverage report
uv run coverage run -m pytest
uv run coverage report
```

**Minimum Coverage:** 50%

Tests are run in CI for Python 3.12, 3.13, and 3.14.

## Database Changes

If you modify the database schema:

```bash
# Create migration
just db-new add_feature_to_users

# Edit the SQL file in db/migrations/

# Test it
just db-up

# Rollback if needed
just db-rollback
```

## Architecture

Omnihub uses Clean Architecture:

```
modules/
├── domain/         # Entities, business logic
├── application/    # Services, use cases
├── infrastructure/ # Database, HTTP, external APIs
└── dependencies/   # Dependency injection
```

When adding a module, follow this structure (see [CLAUDE.md](CLAUDE.md)).

## Pre-commit Hooks

Hooks automatically run before each commit:
- Ruff format check
- Ruff linting
- Type checking (ty)
- Detects trailing whitespace
- Detects private keys

To run manually:
```bash
just pre-commit-check
```

To skip hooks (not recommended):
```bash
git commit --no-verify
```

## PR Requirements

Before submitting a PR, ensure:
- ✓ Passes `just qa` locally
- ✓ Includes tests for new features
- ✓ Updates documentation (CLAUDE.md if architecture changes)
- ✓ Follows Conventional Commits format
- ✓ No merge conflicts with main branch
- ✓ All CI checks pass

## Debugging

### View Database Schema
```bash
docker exec omnihub_postgres psql -U omni_user -d omnihub_dev -c "\d auth.users"
```

### Check Docker Logs
```bash
docker logs omnihub_postgres  # or omnihub_redis
```

### Type Check in Watch Mode
```bash
just type-check-watch
```

### Debug Tests
```bash
just pdb tests/path/to/test.py
```

## Resources

- [CLAUDE.md](CLAUDE.md) - Project architecture & documentation
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Pydantic V2](https://docs.pydantic.dev/2.0/)
- [Ruff](https://docs.astral.sh/ruff/)

## Questions?

- Check existing issues/PRs
- Read CLAUDE.md for architecture details
- Ask in PR comments
- Create a discussion for design questions

---

Thank you for contributing! 🚀
