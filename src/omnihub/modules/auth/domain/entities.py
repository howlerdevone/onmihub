from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID


@dataclass(frozen=True)
class AuthSession:
  id: UUID
  user_id: UUID
  access_token: str | None = None
  refresh_token: str | None = None
  expires_at: datetime | None = None
  created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
  email: str | None = None
