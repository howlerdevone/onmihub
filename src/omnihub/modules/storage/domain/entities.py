from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class StorageObject:
  """Represents a file or object in cloud storage."""

  name: str
  size: int
  updated_at: datetime
  mimetype: str | None = None
