from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from omnihub.common.db.pg_client import PgClient
from omnihub.modules.agents.domain.entities import Run
from omnihub.modules.agents.domain.exceptions import (
  InvalidRunTokenError,
  RunCreationError,
  RunNotFoundError,
)
from omnihub.modules.agents.ports.runs_provider_port import RunsProviderPort


class RunsPgAdapter(RunsProviderPort):
  """PostgreSQL implementation of the runs provider port."""

  def __init__(self, db: PgClient):
    self.db = db

  async def create_run(
    self,
    *,
    workspace_id: UUID,
    user_id: UUID,
    conversation_id: UUID,
    message_id: UUID,
    manifest: dict,
    run_token: str,
  ) -> Run:
    """Create a new agent run."""
    row = await self.db.fetchrow(
      """
      INSERT INTO agents.runs
        (workspace_id, user_id, conversation_id, message_id, manifest, run_token, status)
      VALUES ($1, $2, $3, $4, $5, $6, 'queued')
      RETURNING
        id, workspace_id, user_id, conversation_id, message_id, status, run_token,
        manifest, created_at, completed_at, last_seq, usage
      """,
      workspace_id,
      user_id,
      conversation_id,
      message_id,
      manifest,
      run_token,
    )

    if not row:
      raise RunCreationError("Failed to create run")

    return Run(
      id=row["id"],
      workspace_id=row["workspace_id"],
      user_id=row["user_id"],
      conversation_id=row["conversation_id"],
      message_id=row["message_id"],
      status=row["status"],
      run_token=row["run_token"],
      manifest=row["manifest"],
      created_at=row["created_at"],
      completed_at=row["completed_at"],
      last_seq=row["last_seq"],
      usage=row["usage"],
    )

  async def get_run(
    self,
    *,
    run_id: UUID,
    run_token: str,
  ) -> Run:
    """Fetch a run and validate the access token."""
    row = await self.db.fetchrow(
      """
      SELECT
        id, workspace_id, user_id, conversation_id, message_id, status, run_token,
        manifest, created_at, completed_at, last_seq, usage
      FROM agents.runs
      WHERE id = $1
      """,
      run_id,
    )

    if not row:
      raise RunNotFoundError("Run not found")

    if row["run_token"] != run_token:
      raise InvalidRunTokenError("Invalid run token")

    return Run(
      id=row["id"],
      workspace_id=row["workspace_id"],
      user_id=row["user_id"],
      conversation_id=row["conversation_id"],
      message_id=row["message_id"],
      status=row["status"],
      run_token=row["run_token"],
      manifest=row["manifest"],
      created_at=row["created_at"],
      completed_at=row["completed_at"],
      last_seq=row["last_seq"],
      usage=row["usage"],
    )

  async def list_queued_runs(self) -> list[Run]:
    """List all queued runs (for dispatcher)."""
    rows = await self.db.fetch(
      """
      SELECT
        id, workspace_id, user_id, conversation_id, message_id, status, run_token,
        manifest, created_at, completed_at, last_seq, usage
      FROM agents.runs
      WHERE status = 'queued'
      ORDER BY created_at ASC
      """,
    )

    return [
      Run(
        id=row["id"],
        workspace_id=row["workspace_id"],
        user_id=row["user_id"],
        conversation_id=row["conversation_id"],
        message_id=row["message_id"],
        status=row["status"],
        run_token=row["run_token"],
        manifest=row["manifest"],
        created_at=row["created_at"],
        completed_at=row["completed_at"],
        last_seq=row["last_seq"],
        usage=row["usage"],
      )
      for row in rows
    ]

  async def update_run_status(
    self,
    *,
    run_id: UUID,
    status: str,
    last_seq: int | None = None,
    usage: dict[str, Any] | None = None,
  ) -> Run:
    """Update run status with optional final seq and usage."""
    completed_at = datetime.now(UTC) if status in ("completed", "failed", "cancelled") else None

    row = await self.db.fetchrow(
      """
      UPDATE agents.runs
      SET status = $2, completed_at = $3, last_seq = $4, usage = $5
      WHERE id = $1
      RETURNING
        id, workspace_id, user_id, conversation_id, message_id, status, run_token,
        manifest, created_at, completed_at, last_seq, usage
      """,
      run_id,
      status,
      completed_at,
      last_seq,
      usage,
    )

    if not row:
      raise RunNotFoundError("Run not found")

    return Run(
      id=row["id"],
      workspace_id=row["workspace_id"],
      user_id=row["user_id"],
      conversation_id=row["conversation_id"],
      message_id=row["message_id"],
      status=row["status"],
      run_token=row["run_token"],
      manifest=row["manifest"],
      created_at=row["created_at"],
      completed_at=row["completed_at"],
      last_seq=row["last_seq"],
      usage=row["usage"],
    )
