from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from omnihub.modules.identity.domain.entities import User


@dataclass(frozen=True)
class AuthSession:
  id: UUID
  user_id: UUID
  access_token: str
  refresh_token: str
  expires_at: datetime
  created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
  user: User | None = None
  email: str | None = None
