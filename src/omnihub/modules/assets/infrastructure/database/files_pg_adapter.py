from __future__ import annotations

from uuid import UUID

from omnihub.common.db.pg_client import PgClient
from omnihub.modules.assets.domain.entities import File
from omnihub.modules.assets.domain.exceptions import FileAlreadyExistsError, FileNotFoundError
from omnihub.modules.assets.ports.files_port import FilesPort


class FilesPgAdapter(FilesPort):
  """PostgreSQL implementation of the files port."""

  def __init__(self, db: PgClient):
    self.db = db

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
    try:
      row = await self.db.fetchrow(
        """
        INSERT INTO assets.files
          (workspace_id, owner_id, name, is_folder, parent_id, storage_path, mime_type, size_bytes)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        RETURNING
          id, workspace_id, owner_id, name, is_folder, parent_id, storage_path, mime_type,
          size_bytes, status, created_at, updated_at
        """,
        workspace_id,
        owner_id,
        name,
        is_folder,
        parent_id,
        storage_path,
        mime_type,
        size_bytes,
      )
    except Exception as error:
      # Check if it's a unique constraint violation
      if "unique_filename_per_folder_workspace" in str(error):
        raise FileAlreadyExistsError(f"File '{name}' already exists in this location") from error
      raise

    if not row:
      raise RuntimeError("Failed to create file")

    return File(
      id=row["id"],
      workspace_id=row["workspace_id"],
      owner_id=row["owner_id"],
      name=row["name"],
      is_folder=row["is_folder"],
      parent_id=row["parent_id"],
      storage_path=row["storage_path"],
      mime_type=row["mime_type"],
      size_bytes=row["size_bytes"],
      status=row["status"],
      created_at=row["created_at"],
      updated_at=row["updated_at"],
    )

  async def get_file(self, *, file_id: UUID) -> File:
    """Retrieve a file by ID."""
    row = await self.db.fetchrow(
      """
      SELECT
        id, workspace_id, owner_id, name, is_folder, parent_id, storage_path, mime_type,
        size_bytes, status, created_at, updated_at
      FROM assets.files
      WHERE id = $1
      """,
      file_id,
    )

    if not row:
      raise FileNotFoundError(f"File '{file_id}' not found")

    return File(
      id=row["id"],
      workspace_id=row["workspace_id"],
      owner_id=row["owner_id"],
      name=row["name"],
      is_folder=row["is_folder"],
      parent_id=row["parent_id"],
      storage_path=row["storage_path"],
      mime_type=row["mime_type"],
      size_bytes=row["size_bytes"],
      status=row["status"],
      created_at=row["created_at"],
      updated_at=row["updated_at"],
    )

  async def list_files(self, *, parent_id: UUID | None = None) -> list[File]:
    """List files under a given parent folder."""
    rows = await self.db.fetch(
      """
      SELECT
        id, workspace_id, owner_id, name, is_folder, parent_id, storage_path, mime_type,
        size_bytes, status, created_at, updated_at
      FROM assets.files
      WHERE parent_id = $1
      ORDER BY is_folder DESC, name ASC
      """,
      parent_id,
    )

    return [
      File(
        id=row["id"],
        workspace_id=row["workspace_id"],
        owner_id=row["owner_id"],
        name=row["name"],
        is_folder=row["is_folder"],
        parent_id=row["parent_id"],
        storage_path=row["storage_path"],
        mime_type=row["mime_type"],
        size_bytes=row["size_bytes"],
        status=row["status"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
      )
      for row in rows
    ]
