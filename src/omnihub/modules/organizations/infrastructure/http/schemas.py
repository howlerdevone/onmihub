from __future__ import annotations

from datetime import datetime
from uuid import UUID

from omnihub.common import CustomBaseModel


class CreateWorkspaceRequest(CustomBaseModel):
  name: str
  slug: str | None = None


class WorkspaceResponse(CustomBaseModel):
  id: UUID
  name: str
  slug: str
  is_active: bool
  created_at: datetime
  updated_at: datetime


class OrganizationContextResponse(CustomBaseModel):
  workspace: WorkspaceResponse
  role: str
  permissions: list[str]
