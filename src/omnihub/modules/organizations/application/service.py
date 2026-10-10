from __future__ import annotations

from uuid import UUID, uuid4

from omnihub.common import slugify
from omnihub.modules.organizations.domain.entities import OrganizationContext, Workspace
from omnihub.modules.organizations.ports.workspace_provider_port import WorkspaceProviderPort
from omnihub.modules.storage.application.service import StorageApplicationService


class OrganizationsApplicationService:
  """Application service orchestrating workspace lifecycle workflows."""

  def __init__(
    self,
    workspace_provider: WorkspaceProviderPort,
    storage_service: StorageApplicationService,
  ) -> None:
    self.workspace_provider = workspace_provider
    self.storage_service = storage_service

  async def create_workspace(
    self,
    *,
    user_id: UUID,
    name: str,
    slug: str | None = None,
  ) -> Workspace:
    """Create a workspace and assign the owner membership with default permissions."""
    base_slug = slug or slugify(name)
    workspace_slug = f"{base_slug}-{user_id.hex[:8]}"

    return await self.workspace_provider.create_workspace(
      user_id=user_id,
      name=name,
      slug=workspace_slug,
      role="owner",
    )

  async def create_workspace_with_apps(
    self,
    *,
    user_id: UUID,
    name: str,
    slug: str | None = None,
    app_ids: list[str],
  ) -> tuple[Workspace, list[str]]:
    """Provision storage, then atomically persist the workspace and everything that hangs off it."""
    base_slug = slug or slugify(name)
    workspace_slug = f"{base_slug}-{user_id.hex[:8]}"

    # Rejected up front so a routine 409 does not leave a provisioned folder behind.
    await self.workspace_provider.user_can_create_workspace(user_id=user_id, name=name)

    # Minted here so storage is provisioned before anything is committed.
    workspace_id = uuid4()

    await self.storage_service.execute_create_workspace_folder(
      workspace_id=str(workspace_id),
      user_id=str(user_id),
    )

    return await self.workspace_provider.create_workspace_with_apps(
      workspace_id=workspace_id,
      user_id=user_id,
      name=name,
      slug=workspace_slug,
      app_ids=app_ids,
      storage_path=f"{workspace_id}/{user_id}/",
      role="owner",
    )

  async def get_workspace(
    self,
    *,
    workspace_id: UUID,
    user_id: UUID,
  ) -> OrganizationContext:
    """Fetch a workspace context and enforce membership-based access."""
    return await self.workspace_provider.get_workspace_for_user(
      workspace_id=workspace_id,
      user_id=user_id,
    )

  async def list_workspaces(
    self,
    *,
    user_id: UUID,
  ) -> list[Workspace]:
    """List all workspaces the user is a member of."""
    return await self.workspace_provider.list_workspaces_for_user(user_id=user_id)
