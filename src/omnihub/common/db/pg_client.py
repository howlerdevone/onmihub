from __future__ import annotations

import contextlib
from collections.abc import AsyncIterator
from types import TracebackType
from typing import Any

import asyncpg


class PgTransaction:
  """Executes queries within a single asyncpg transaction."""

  def __init__(self, connection: asyncpg.Connection | asyncpg.pool.PoolConnectionProxy):
    self.connection = connection

  async def execute(self, query: str, *args: Any) -> Any:
    # Execute a query and return the result.
    return await self.connection.execute(query, *args)

  async def fetch(self, query: str, *args: Any) -> list[asyncpg.Record]:
    # Fetch all rows matching the query.
    return await self.connection.fetch(query, *args)

  async def fetchrow(self, query: str, *args: Any) -> asyncpg.Record | None:
    # Fetch a single row or None if not found.
    return await self.connection.fetchrow(query, *args)

  async def fetchval(self, query: str, *args: Any) -> Any:
    # Fetch a single scalar value.
    return await self.connection.fetchval(query, *args)


class PgClient:
  def __init__(self, dsn: str):
    self.dsn = dsn
    self.pool: asyncpg.Pool | None = None

  async def __aenter__(self) -> PgClient:
    self.pool = await asyncpg.create_pool(dsn=self.dsn)
    return self

  async def __aexit__(
    self,
    exc_type: type[BaseException] | None,
    exc_val: BaseException | None,
    exc_tb: TracebackType | None,
  ) -> None:
    if self.pool:
      await self.pool.close()

  async def execute(self, query: str, *args: Any) -> Any:
    # Execute a query on a pooled connection.
    if not self.pool:
      raise RuntimeError("Database connection pool is not initialized.")
    async with self.pool.acquire() as connection:
      return await connection.execute(query, *args)

  async def fetch(self, query: str, *args: Any) -> list[asyncpg.Record]:
    # Fetch all rows from a query on a pooled connection.
    if not self.pool:
      raise RuntimeError("Database connection pool is not initialized.")
    async with self.pool.acquire() as connection:
      return await connection.fetch(query, *args)

  async def fetchrow(self, query: str, *args: Any) -> asyncpg.Record | None:
    # Fetch a single row from a query on a pooled connection.
    if not self.pool:
      raise RuntimeError("Database connection pool is not initialized.")
    async with self.pool.acquire() as connection:
      return await connection.fetchrow(query, *args)

  async def fetchval(self, query: str, *args: Any) -> Any:
    # Fetch a single scalar value from a query on a pooled connection.
    if not self.pool:
      raise RuntimeError("Database connection pool is not initialized.")
    async with self.pool.acquire() as connection:
      return await connection.fetchval(query, *args)

  @contextlib.asynccontextmanager
  async def transaction(self) -> AsyncIterator[PgTransaction]:
    # Return an async context manager for atomic multi-statement transactions.
    if not self.pool:
      raise RuntimeError("Database connection pool is not initialized.")
    async with self.pool.acquire() as connection:
      async with connection.transaction():
        yield PgTransaction(connection)
