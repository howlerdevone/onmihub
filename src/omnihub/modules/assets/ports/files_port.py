from __future__ import annotations

from typing import Protocol
from uuid import UUID

from omnihub.modules.assets.domain.entities import File


class FilesPort(Protocol):
  """Architectural port defining file/folder persistence operations."""

  async def create_file(
    self,
    *,
    workspace_id: UUID,
    owner_id: UUID,
    name: str,
    is_folder: bool,
    parent_id: UUID | None = None,
    storage_path: str | None = None,
    mime_type: str | None = None,
    size_bytes: int = 0,
  ) -> File:
    """Create a new file or folder record."""
    ...

  async def get_file(self, *, file_id: UUID) -> File:
    """Retrieve a file by ID."""
    ...

  async def list_files(self, *, parent_id: UUID | None = None) -> list[File]:
    """List files under a given parent folder."""
    ...
