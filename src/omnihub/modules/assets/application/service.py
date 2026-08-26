from __future__ import annotations

from uuid import UUID

from omnihub.modules.assets.domain.entities import File
from omnihub.modules.assets.ports.files_port import FilesPort


class FilesApplicationService:
  """Application service orchestrating file/folder management workflows."""

  def __init__(self, files_provider: FilesPort) -> None:
    self.files_provider = files_provider

  async def execute_create_folder(
    self,
    *,
    workspace_id: UUID,
    owner_id: UUID,
    name: str,
    parent_id: UUID | None = None,
    storage_path: str | None = None,
  ) -> File:
    """Create a folder record.

    Args:
      workspace_id: The UUID of the workspace.
      owner_id: The UUID of the folder owner (user).
      name: The folder name.
      parent_id: The parent folder UUID (if nested).
      storage_path: The GCS path to the folder.

    Returns:
      The created File entity (with is_folder=True).
    """
    return await self.files_provider.create_file(
      workspace_id=workspace_id,
      owner_id=owner_id,
      name=name,
      is_folder=True,
      parent_id=parent_id,
      storage_path=storage_path,
    )

  async def execute_create_file(
    self,
    *,
    workspace_id: UUID,
    owner_id: UUID,
    name: str,
    parent_id: UUID | None = None,
    storage_path: str | None = None,
    mime_type: str | None = None,
    size_bytes: int = 0,
  ) -> File:
    """Create a file record.

    Args:
      workspace_id: The UUID of the workspace.
      owner_id: The UUID of the file owner (user).
      name: The file name.
      parent_id: The parent folder UUID.
      storage_path: The GCS path to the file.
      mime_type: The MIME type of the file.
      size_bytes: The file size in bytes.

    Returns:
      The created File entity (with is_folder=False).
    """
    return await self.files_provider.create_file(
      workspace_id=workspace_id,
      owner_id=owner_id,
      name=name,
      is_folder=False,
      parent_id=parent_id,
      storage_path=storage_path,
      mime_type=mime_type,
      size_bytes=size_bytes,
    )

  async def execute_get_file(self, *, file_id: UUID) -> File:
    """Retrieve a file by ID.

    Args:
      file_id: The UUID of the file.

    Returns:
      The File entity.

    Raises:
      FileNotFoundError: If the file does not exist.
    """
    return await self.files_provider.get_file(file_id=file_id)

  async def execute_list_files(self, *, parent_id: UUID | None = None) -> list[File]:
    """List files under a parent folder.

    Args:
      parent_id: The parent folder UUID (None for root).

    Returns:
      List of File entities under the parent.
    """
    return await self.files_provider.list_files(parent_id=parent_id)
