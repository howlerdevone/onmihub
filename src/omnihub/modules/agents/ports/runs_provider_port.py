from typing import Any, Protocol
from uuid import UUID

from omnihub.modules.agents.domain.entities import Run


class RunsProviderPort(Protocol):
  """Architectural port defining agent run persistence operations."""

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
    ...

  async def get_run(
    self,
    *,
    run_id: UUID,
    run_token: str,
  ) -> Run:
    """Fetch a run and validate the access token."""
    ...

  async def list_queued_runs(self) -> list[Run]:
    """List all queued runs (for dispatcher)."""
    ...

  async def update_run_status(
    self,
    *,
    run_id: UUID,
    status: str,
    last_seq: int | None = None,
    usage: dict[str, Any] | None = None,
  ) -> Run:
    """Update run status with optional final seq and usage."""
    ...
