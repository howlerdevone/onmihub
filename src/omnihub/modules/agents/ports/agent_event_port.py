from typing import Any, Protocol
from uuid import UUID


class AgentEventPort(Protocol):
  """Architectural port for agent event persistence."""

  async def create_event(
    self,
    *,
    run_id: UUID,
    event_type: str,
    data: dict[str, Any],
  ) -> None:
    """Record an event for audit trail."""
    ...
