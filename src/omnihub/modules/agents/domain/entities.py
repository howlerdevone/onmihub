from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass
class Run:
  id: UUID
  workspace_id: UUID
  user_id: UUID
  conversation_id: UUID
  message_id: UUID
  status: str  # 'queued', 'running', 'completed', 'failed', 'cancelled'
  run_token: str
  manifest: dict[str, Any]
  created_at: datetime
  completed_at: datetime | None = None
  last_seq: int | None = None
  usage: dict[str, Any] | None = None
