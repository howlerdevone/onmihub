from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class User:
  id: UUID
  email: str
  firstname: str | None = None
  lastname: str | None = None
  preferred_language: str | None = None
  timezone: str | None = None
  onboarding_completed_at: datetime | None = None
  access_token: str | None = None
  refresh_token: str | None = None
