from __future__ import annotations

from uuid import UUID

from omnihub.common import slugify
from omnihub.modules.organizations.domain.entities import OrganizationContext, Workspace
from omnihub.modules.organizations.ports.workspace_provider_port import WorkspaceProviderPort


class OrganizationsApplicationService:
  """Application service orchestrating workspace lifecycle workflows."""

  def __init__(self, workspace_provider: WorkspaceProviderPort) -> None:
    self.workspace_provider = workspace_provider

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
