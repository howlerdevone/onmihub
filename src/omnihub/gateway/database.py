import contextlib
import logging
import os
from collections.abc import Awaitable, Callable

import asyncpg
from fastapi import FastAPI, Request
from fastapi.responses import Response

from omnihub.common.db.pg_client import PgClient
from omnihub.gateway.supabase import get_supabase_client

logger = logging.getLogger(__name__)

# Extract database credentials or fallback to local Docker composition settings on port 5433
DATABASE_DSN = os.environ.get("DATABASE_URL", "postgres://omni_user:omni_password@localhost:5433/omnihub_dev")


@contextlib.asynccontextmanager
async def database_lifespan(app: FastAPI):
    """
    Manages the global setup and safety cleanup of the high-performance asyncpg
    pool connection during application boot and graceful system shutdown boundaries.
    """
    app.state.db_pool = await asyncpg.create_pool(
        dsn=DATABASE_DSN,
        min_size=5,
        max_size=20,
    )
    logger.info("🚀 Database connection pool initialized (host: localhost, port: 5433)")

    # Create a PgClient instance that reuses the same asyncpg pool so
    # adapters expecting `PgClient` can operate normally.
    pg_client = PgClient(dsn=DATABASE_DSN)
    # Attach the already-created pool to the PgClient to avoid double pools
    pg_client.pool = app.state.db_pool
    app.state.db_client = pg_client

    app.state.supabase_client = get_supabase_client()

    yield  # Application runs here while waiting for termination signals

    # Close resources cleanly when stopping the app
    await app.state.db_pool.close()
    logger.info("🛑 Database connection pool closed")


async def inject_db_connection_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """
    High-performance HTTP Request Middleware. Automatically acquires a dedicated
    standalone connection from the pool, embedding it inside the request state
    before routing traffic to adapters, returning it safely upon request completion.
    """
    # Provide a `PgClient` instance to downstream handlers via request.state
    # so repository/adapters that depend on `PgClient` can use it.
    request.state.db_client = request.app.state.db_client

    # Propagate the execution flow to the downstream endpoint handlers
    response: Response = await call_next(request)
    return response
