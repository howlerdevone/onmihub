from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class File:
  """Represents a file or folder in the asset storage."""

  id: UUID
  workspace_id: UUID
  owner_id: UUID
  name: str
  is_folder: bool
  parent_id: UUID | None = None
  storage_path: str | None = None
  mime_type: str | None = None
  size_bytes: int = 0
  status: str = "ready"
  created_at: datetime | None = None
  updated_at: datetime | None = None
