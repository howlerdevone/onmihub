from __future__ import annotations

from fastapi import Depends, Request

from omnihub.common.db.pg_client import PgClient
from omnihub.modules.assets.application.service import FilesApplicationService
from omnihub.modules.assets.infrastructure.database.files_pg_adapter import FilesPgAdapter
from omnihub.modules.assets.ports.files_port import FilesPort


def get_files_provider(request: Request) -> FilesPort:
  """Return the current files provider implementation."""
  db_client: PgClient = request.state.db_client
  return FilesPgAdapter(db=db_client)


async def get_files_service(
  files_provider: FilesPort = Depends(get_files_provider),
) -> FilesApplicationService:
  """Composition root for files workflows using the active database provider."""
  return FilesApplicationService(files_provider=files_provider)
