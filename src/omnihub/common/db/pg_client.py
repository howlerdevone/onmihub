from __future__ import annotations
from types import TracebackType
from typing import Any, Optional

import asyncpg

class PgClient:
  def __init__(self, dsn: str):
    self.dsn = dsn
    self.pool: asyncpg.Pool | None = None

  async def __aenter__(self) -> PgClient:
    self.pool: asyncpg.Pool = await asyncpg.create_pool(dsn=self.dsn)  # type: ignore
    return self

  async def __aexit__(self, exc_type: type | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:
    if self.pool:
      await self.pool.close()

  async def execute(self, query: str, *args: Any) -> Any:
    if not self.pool:
      raise RuntimeError("Database connection pool is not initialized.")
    async with self.pool.acquire() as connection:
      return await connection.execute(query, *args)

  async def fetch(self, query: str, *args: Any) -> list[asyncpg.Record]:
    if not self.pool:
      raise RuntimeError("Database connection pool is not initialized.")
    async with self.pool.acquire() as connection:
      return await connection.fetch(query, *args)
    
  async def fetchrow(self, query: str, *args: Any) -> Optional[asyncpg.Record]:
    if not self.pool:
      raise RuntimeError("Database connection pool is not initialized.")
    async with self.pool.acquire() as connection:
      return await connection.fetchrow(query, *args)
  
  async def fetchval(self, query: str, *args: Any) -> Any:
    if not self.pool:
      raise RuntimeError("Database connection pool is not initialized.")
    async with self.pool.acquire() as connection:
      return await connection.fetchval(query, *args)
    