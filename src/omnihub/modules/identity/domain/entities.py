from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class User:
    id: UUID
    email: str
    display_name: str | None = None
    preferred_language: str | None = None
    timezone: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None
