from __future__ import annotations

from datetime import datetime

from google.cloud.exceptions import NotFound

from omnihub.common.storage import GcsClient
from omnihub.modules.storage.domain.entities import StorageObject
from omnihub.modules.storage.domain.exceptions import (
  StorageObjectNotFoundError,
  StorageProvisioningError,
)
from omnihub.modules.storage.ports.storage_provider_port import StorageProviderPort


class StorageGcsAdapter(StorageProviderPort):
  """Google Cloud Storage implementation of the storage provider port."""

  def __init__(self, client: GcsClient):
    self.client = client

  async def create_folder(self, *, path: str) -> None:
    """Create a folder marker at the given path."""
    try:
      await self.client.create_folder(path)
    except Exception as error:
      raise StorageProvisioningError(f"Failed to provision storage folder at '{path}'") from error

  async def list_objects(self, *, path: str) -> list[StorageObject]:
    """List all objects under the given prefix path."""
    blobs = await self.client.list_blobs(prefix=path)
    return [
      StorageObject(
        name=blob.name,  # type: ignore
        size=blob.size or 0,
        updated_at=blob.updated or datetime.now(),
        mimetype=blob.content_type,
      )
      for blob in blobs
    ]

  async def get_object(self, *, path: str) -> bytes:
    """Download an object's contents as bytes."""
    try:
      return await self.client.get_blob_bytes(path)
    except NotFound as error:
      raise StorageObjectNotFoundError(f"Object not found at '{path}'") from error
