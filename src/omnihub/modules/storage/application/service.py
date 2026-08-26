from __future__ import annotations

from omnihub.modules.storage.domain.entities import StorageObject
from omnihub.modules.storage.ports.storage_provider_port import StorageProviderPort


class StorageApplicationService:
  """Application service orchestrating storage provisioning workflows."""

  def __init__(self, storage_provider: StorageProviderPort) -> None:
    self.storage_provider = storage_provider

  async def execute_create_workspace_folder(self, *, workspace_id: str, user_id: str) -> None:
    """Create a folder for a workspace owned by a user.

    Args:
      workspace_id: The UUID of the workspace.
      user_id: The UUID of the workspace owner.

    Raises:
      StorageProvisioningError: If folder provisioning fails.
    """
    path = f"{workspace_id}/{user_id}/"
    await self.storage_provider.create_folder(path=path)

  async def execute_list_workspace_objects(self, *, workspace_id: str, user_id: str) -> list[StorageObject]:
    """List all objects under a workspace folder.

    Args:
      workspace_id: The UUID of the workspace.
      user_id: The UUID of the user (workspace owner or member).

    Returns:
      List of storage objects under the workspace path.
    """
    path = f"{workspace_id}/{user_id}/"
    return await self.storage_provider.list_objects(path=path)

  async def execute_get_workspace_object(self, *, workspace_id: str, user_id: str, object_key: str) -> bytes:
    """Download an object from a workspace folder.

    Args:
      workspace_id: The UUID of the workspace.
      user_id: The UUID of the user (workspace owner or member).
      object_key: The key/name of the object relative to the workspace folder.

    Returns:
      The object contents as bytes.

    Raises:
      StorageObjectNotFoundError: If the object does not exist.
    """
    path = f"{workspace_id}/{user_id}/{object_key}"
    return await self.storage_provider.get_object(path=path)
