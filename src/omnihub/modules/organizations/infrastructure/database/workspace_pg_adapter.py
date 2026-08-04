from __future__ import annotations

from uuid import UUID

from omnihub.common.db.pg_client import PgClient
from omnihub.modules.organizations.domain.entities import OrganizationContext, Workspace
from omnihub.modules.organizations.domain.exceptions import (
  OrganizationAccessDeniedError,
  OrganizationAlreadyExistsError,
  OrganizationNotFoundError,
)
from omnihub.modules.organizations.ports.workspace_provider_port import WorkspaceProviderPort


class WorkspacePgAdapter(WorkspaceProviderPort):
  """PostgreSQL implementation of the organizations workspace port."""

  def __init__(self, db: PgClient):
    self.db = db

  async def create_workspace(
    self,
    *,
    user_id: UUID,
    name: str,
    slug: str,
    role: str = "owner",
  ) -> Workspace:
    """Create a workspace only if this user does not already own one with the same name."""
    existing_workspace = await self.db.fetchrow(
      """
      SELECT w.id
      FROM organizations.workspaces w
      INNER JOIN organizations.memberships m ON m.workspace_id = w.id
      WHERE m.user_id = $1
        AND lower(w.name) = lower($2)
      LIMIT 1
      """,
      user_id,
      name,
    )

    if existing_workspace:
      raise OrganizationAlreadyExistsError(f"Workspace '{name}' already exists for this user")

    try:
      workspace_row = await self.db.fetchrow(
        """
        INSERT INTO organizations.workspaces (name, slug, created_by)
        VALUES ($1, $2, $3)
        RETURNING id, name, slug, is_active, created_at, updated_at
        """,
        name,
        slug,
        user_id,
      )
    except Exception as error:
      error_code = getattr(error, "sqlstate", None) or getattr(error, "code", None)
      if error_code == "23505":
        raise OrganizationAlreadyExistsError(f"Workspace slug '{slug}' already exists") from error
      raise

    if not workspace_row:
      raise RuntimeError("Failed to create workspace")

    await self.db.execute(
      """
      INSERT INTO organizations.memberships (workspace_id, user_id, role)
      VALUES ($1, $2, $3)
      """,
      workspace_row["id"],
      user_id,
      role,
    )

    return Workspace(
      id=workspace_row["id"],
      name=workspace_row["name"],
      slug=workspace_row["slug"],
      is_active=workspace_row["is_active"],
      created_at=workspace_row["created_at"],
      updated_at=workspace_row["updated_at"],
    )

  async def get_workspace_for_user(
    self,
    *,
    workspace_id: UUID,
    user_id: UUID,
  ) -> OrganizationContext:
    """Fetch a workspace and the authenticated user's role and permissions."""
    row = await self.db.fetchrow(
      """
      SELECT
        w.id,
        w.name,
        w.slug,
        w.is_active,
        w.created_at,
        w.updated_at,
        m.role
      FROM organizations.workspaces w
      LEFT JOIN organizations.memberships m
        ON m.workspace_id = w.id AND m.user_id = $2
      WHERE w.id = $1
      """,
      workspace_id,
      user_id,
    )

    if not row:
      raise OrganizationNotFoundError("Workspace not found")

    role = row["role"]
    if role is None:
      raise OrganizationAccessDeniedError("User is not a member of this workspace")

    permission_rows = await self.db.fetch(
      """
      SELECT rp.permission_id
      FROM organizations.role_permissions rp
      WHERE rp.role = $1::organizations.workspace_role_enum
      ORDER BY rp.permission_id ASC
      """,
      role,
    )

    permissions = [perm["permission_id"] for perm in permission_rows]

    workspace = Workspace(
      id=row["id"],
      name=row["name"],
      slug=row["slug"],
      is_active=row["is_active"],
      created_at=row["created_at"],
      updated_at=row["updated_at"],
    )

    return OrganizationContext(workspace=workspace, role=str(role), permissions=permissions)
