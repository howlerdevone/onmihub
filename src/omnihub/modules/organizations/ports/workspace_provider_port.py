from __future__ import annotations

from typing import Protocol
from uuid import UUID

from omnihub.modules.organizations.domain.entities import OrganizationContext, Workspace


class WorkspaceProviderPort(Protocol):
  """Architectural port defining workspace persistence operations."""

  async def create_workspace(
    self,
    *,
    user_id: UUID,
    name: str,
    slug: str,
    role: str = "owner",
  ) -> Workspace:
    """Create a workspace and assign the initial role to the owner user."""
    ...

  async def get_workspace_for_user(
    self,
    *,
    workspace_id: UUID,
    user_id: UUID,
  ) -> OrganizationContext:
    """Return a workspace plus the caller's role and permissions."""
    ...

  async def create_workspace_with_apps(
    self,
    *,
    user_id: UUID,
    name: str,
    slug: str,
    app_ids: list[str],
    role: str = "owner",
  ) -> tuple[Workspace, list[str]]:
    """Atomically create workspace, owner membership, and link selected apps."""
    ...
