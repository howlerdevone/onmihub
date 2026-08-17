# Justfile for omnihub

# On Windows, run recipes with PowerShell so devs don't need Git Bash / sh.
# macOS and Linux keep the default sh.
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

# Enable doppler-env auto-injection for every Python process launched by this
# justfile. The doppler-env .pth hook is a no-op unless DOPPLER_ENV is set, so
# this line is what wires our commands to Doppler. Non-Python tools (dbmate)
# are still wrapped explicitly with `doppler run --` below.
export DOPPLER_ENV := "1"


# ------------------------------------------------------------------------------
# INFRASTRUCTURE (Docker)
# ------------------------------------------------------------------------------

# Start Postgres and Redis services in the background
docker-up:
    docker compose up -d

# Stop Docker services without removing data
docker-down:
    docker compose down

# Shut down services and remove volumes (full cleanup)
docker-destroy:
    docker compose down -v

# ------------------------------------------------------------------------------
# DATABASE & MIGRATIONS (dbmate)
# ------------------------------------------------------------------------------

# Create a new migration (e.g.: just db-new create_users_table)
db-new NAME:
    dbmate new {{NAME}}

# Ensure Docker is running and apply all pending migrations
db-up: docker-up
    @echo "Waiting for Postgres to respond..."
    @sleep 2
    doppler run -- dbmate up

# Roll back the last applied migration
db-rollback:
    doppler run -- dbmate rollback

# Show the current migrations status
db-status:
    doppler run -- dbmate status

# ------------------------------------------------------------------------------
# PRE-COMMIT & GIT HOOKS
# ------------------------------------------------------------------------------

# Install pre-commit hooks
pre-commit-install:
    pip install pre-commit
    pre-commit install
    @echo "✓ Pre-commit hooks installed"

# Run pre-commit on all files
pre-commit-check:
    pre-commit run --all-files

# Uninstall pre-commit hooks
pre-commit-uninstall:
    pre-commit uninstall

# Show available commands
list:
    @just --list

alias b := build
alias c := clean
alias d := docs-serve
alias t := test
alias tc := type-check

# Type check the project with ty
type-check:
    uv run --python=3.14 ty check .

# Type check with concise output (one diagnostic per line)
type-check-concise:
    uv run --python=3.14 ty check --output-format=concise .

# Type check in watch mode (rechecks on file changes)
type-check-watch:
    uv run --python=3.14 ty check --watch .

# Run all the formatting, linting, and testing commands
qa:
    uv run --python=3.14 ruff format .
    uv run --python=3.14 ruff check . --fix
    uv run --python=3.14 ruff check --select I --fix .
    uv run --python=3.14 ty check --output-format=concise .
    uv run --python=3.14 pytest

# Run all the tests for all the supported Python versions
testall:
    uv run --python=3.12 pytest
    uv run --python=3.13 pytest
    uv run --python=3.14 pytest

# Run all the tests, but allow for arguments to be passed
test *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run --python=3.14 pytest {{ARGS}}

# Run all the tests, but on failure, drop into the debugger
pdb *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run --python=3.14 pytest --pdb --maxfail=10 {{ARGS}}

# Run tests with coverage across all supported Python versions
coverage:
    uv run --python=3.12 coverage run -m pytest
    uv run --python=3.13 coverage run -m pytest
    uv run --python=3.14 coverage run -m pytest
    uv run --python=3.14 coverage combine
    uv run --python=3.14 coverage report
    uv run --python=3.14 coverage html

# Serve docs locally with live reload (macOS / Linux)
[unix]
docs-serve:
    -lsof -ti :8000 | xargs kill
    uv run --group docs zensical serve

# Serve docs locally with live reload (Windows)
[windows]
docs-serve:
    -Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
    uv run --group docs zensical serve

# Build docs (strict mode, fails on warnings)
docs-build:
    uv run --group docs zensical build --clean

# Build the project, useful for checking that packaging is correct (macOS / Linux)
[unix]
build:
    rm -rf build
    rm -rf dist
    uv build

# Build the project, useful for checking that packaging is correct (Windows)
[windows]
build:
    if (Test-Path build) { Remove-Item -Recurse -Force build }
    if (Test-Path dist)  { Remove-Item -Recurse -Force dist }
    uv build

# Tag, push, and create a GitHub release
release:
    uv run scripts/release.py

# Remove all build, test, coverage and Python artifacts
clean: clean-build clean-pyc clean-test

# Remove build artifacts (macOS / Linux)
[unix]
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

# Remove build artifacts (Windows)
[windows]
clean-build:
    if (Test-Path build) { Remove-Item -Recurse -Force build }
    if (Test-Path dist)  { Remove-Item -Recurse -Force dist }
    if (Test-Path .eggs) { Remove-Item -Recurse -Force .eggs }
    Get-ChildItem -Path . -Recurse -Directory -Filter '*.egg-info' -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
    Get-ChildItem -Path . -Recurse -File -Filter '*.egg' -ErrorAction SilentlyContinue | Remove-Item -Force

# Remove Python file artifacts (macOS / Linux)
[unix]
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

# Remove Python file artifacts (Windows)
[windows]
clean-pyc:
    Get-ChildItem -Path . -Recurse -File -Include '*.pyc','*.pyo','*~' -ErrorAction SilentlyContinue | Remove-Item -Force
    Get-ChildItem -Path . -Recurse -Directory -Filter '__pycache__' -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force

# Remove test and coverage artifacts (macOS / Linux)
[unix]
clean-test:
	rm -f .coverage
	rm -f .coverage.*
	rm -fr htmlcov/
	rm -fr .pytest_cache

# Remove test and coverage artifacts (Windows)
[windows]
clean-test:
    Remove-Item -Force -ErrorAction SilentlyContinue .coverage
    Get-ChildItem -Force -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -like '.coverage.*' } | Remove-Item -Force
    if (Test-Path htmlcov)       { Remove-Item -Recurse -Force htmlcov }
    if (Test-Path .pytest_cache) { Remove-Item -Recurse -Force .pytest_cache }

# Publish to PyPI (manual alternative to GitHub Actions)
publish:
    uv build
    uv publish

# Start the FastAPI development server with auto-reload (macOS / Linux)
[unix]
dev:
    OMNIHUB_RELOAD=true uv run python -m omnihub

# Start the FastAPI development server with auto-reload (Windows)
[windows]
dev:
    $env:OMNIHUB_RELOAD="true"; uv run python -m omnihub

# Start the Celery worker (change 'config' to your celery module name)
worker:
    uv run celery -A main.celery_app worker --loglevel=info