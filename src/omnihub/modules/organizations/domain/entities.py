from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class Workspace:
  id: UUID
  name: str
  slug: str
  is_active: bool
  created_at: datetime
  updated_at: datetime


@dataclass(slots=True)
class OrganizationContext:
  workspace: Workspace
  role: str
  permissions: list[str]
