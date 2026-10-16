import contextlib
import logging
from collections.abc import Awaitable, Callable

import asyncpg
from fastapi import FastAPI, Request
from fastapi.responses import Response

from omnihub.common.db.pg_client import PgClient
from omnihub.config.settings import DATABASE_URL
from omnihub.gateway.gcs_storage import get_gcs_client
from omnihub.gateway.supabase import get_supabase_client


logger = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI):
  """
  Manages the global setup and safety cleanup of all shared services
  (database, authentication, storage) during application boot and graceful shutdown.
  """
  app.state.db_pool = await asyncpg.create_pool(
    dsn=DATABASE_URL,
    min_size=5,
    max_size=20,
  )
  logger.info("🚀 Database connection pool initialized (host: localhost, port: 5433)")

  # Create a PgClient instance that reuses the same asyncpg pool so
  # adapters expecting `PgClient` can operate normally.
  pg_client = PgClient(dsn=DATABASE_URL)
  # Attach the already-created pool to the PgClient to avoid double pools
  pg_client.pool = app.state.db_pool
  app.state.db_client = pg_client

  app.state.supabase_client = await get_supabase_client()

  app.state.gcs_client = get_gcs_client()

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
