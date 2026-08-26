from __future__ import annotations

from fastapi import Depends, Request

from omnihub.common.storage import GcsClient
from omnihub.modules.storage.application.service import StorageApplicationService
from omnihub.modules.storage.infrastructure.gcs.storage_gcs_adapter import StorageGcsAdapter
from omnihub.modules.storage.ports.storage_provider_port import StorageProviderPort


def get_storage_provider(request: Request) -> StorageProviderPort:
  """Return the current storage provider implementation."""
  gcs_client: GcsClient = request.app.state.gcs_client
  return StorageGcsAdapter(client=gcs_client)


async def get_storage_service(
  storage_provider: StorageProviderPort = Depends(get_storage_provider),
) -> StorageApplicationService:
  """Composition root for storage workflows using the active GCS provider."""
  return StorageApplicationService(storage_provider=storage_provider)
