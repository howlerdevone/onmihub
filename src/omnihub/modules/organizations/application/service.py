from __future__ import annotations

from uuid import UUID

from omnihub.common import slugify
from omnihub.modules.assets.application.service import FilesApplicationService
from omnihub.modules.organizations.domain.entities import OrganizationContext, Workspace
from omnihub.modules.organizations.ports.workspace_provider_port import WorkspaceProviderPort
from omnihub.modules.storage.application.service import StorageApplicationService


class OrganizationsApplicationService:
  """Application service orchestrating workspace lifecycle workflows."""

  def __init__(
    self,
    workspace_provider: WorkspaceProviderPort,
    storage_service: StorageApplicationService,
    files_service: FilesApplicationService,
  ) -> None:
    self.workspace_provider = workspace_provider
    self.storage_service = storage_service
    self.files_service = files_service

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
    """Atomically create workspace with apps and assign owner membership."""
    base_slug = slug or slugify(name)
    workspace_slug = f"{base_slug}-{user_id.hex[:8]}"

    workspace, app_ids = await self.workspace_provider.create_workspace_with_apps(
      user_id=user_id,
      name=name,
      slug=workspace_slug,
      app_ids=app_ids,
      role="owner",
    )

    await self.storage_service.execute_create_workspace_folder(
      workspace_id=str(workspace.id),
      user_id=str(user_id),
    )

    storage_path = f"{workspace.id}/{user_id}/"
    await self.files_service.execute_create_folder(
      workspace_id=workspace.id,
      owner_id=user_id,
      name=workspace.slug,
      storage_path=storage_path,
    )

    return workspace, app_ids

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

  async def complete_onboarding(
    self,
    *,
    user_id: UUID,
  ) -> None:
    """Mark the user's onboarding as complete."""
    await self.workspace_provider.mark_user_onboarding_complete(user_id=user_id)
