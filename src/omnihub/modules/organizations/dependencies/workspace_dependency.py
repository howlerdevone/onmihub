from fastapi import Depends, Request

from omnihub.common.db.pg_client import PgClient
from omnihub.modules.assets.dependencies.files_dependency import get_files_service
from omnihub.modules.organizations.application.service import OrganizationsApplicationService
from omnihub.modules.organizations.infrastructure.database.workspace_pg_adapter import WorkspacePgAdapter
from omnihub.modules.organizations.ports.workspace_provider_port import WorkspaceProviderPort
from omnihub.modules.storage.application.service import StorageApplicationService
from omnihub.modules.storage.dependencies.storage_dependency import get_storage_service


def get_workspace_provider(request: Request) -> WorkspaceProviderPort:
  """Return the current workspace provider implementation."""
  db_client: PgClient = request.state.db_client
  return WorkspacePgAdapter(db=db_client)


async def get_organizations_service(
  workspace_provider: WorkspaceProviderPort = Depends(get_workspace_provider),
  storage_service: StorageApplicationService = Depends(get_storage_service),
  files_service=Depends(get_files_service),
) -> OrganizationsApplicationService:
  """Composition root for organizations workflows using workspace, storage, and files services."""
  return OrganizationsApplicationService(
    workspace_provider=workspace_provider,
    storage_service=storage_service,
    files_service=files_service,
  )
