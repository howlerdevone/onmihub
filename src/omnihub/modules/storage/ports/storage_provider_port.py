from __future__ import annotations

from typing import Protocol

from omnihub.modules.storage.domain.entities import StorageObject


class StorageProviderPort(Protocol):
  """Architectural port defining cloud storage operations."""

  async def create_folder(self, *, path: str) -> None:
    """Create a folder marker at the given path."""
    ...

  async def list_objects(self, *, path: str) -> list[StorageObject]:
    """List all objects under the given prefix path."""
    ...

  async def get_object(self, *, path: str) -> bytes:
    """Download an object's contents as bytes."""
    ...
