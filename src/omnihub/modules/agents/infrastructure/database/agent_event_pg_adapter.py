from typing import Any
from uuid import UUID

from omnihub.common.db.pg_client import PgClient
from omnihub.modules.agents.ports.agent_event_port import AgentEventPort


class AgentEventPgAdapter(AgentEventPort):
  """PostgreSQL implementation of the agent event port."""

  def __init__(self, db: PgClient):
    self.db = db

  async def create_event(
    self,
    *,
    run_id: UUID,
    event_type: str,
    data: dict[str, Any],
  ) -> None:
    """Record an event for audit trail."""
    await self.db.execute(
      """
      INSERT INTO agents.events (run_id, event_type, data)
      VALUES ($1, $2, $3)
      """,
      run_id,
      event_type,
      data,
    )
