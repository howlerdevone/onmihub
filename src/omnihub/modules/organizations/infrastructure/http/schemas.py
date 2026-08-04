from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateWorkspaceRequest(BaseModel):
  name: str
  slug: str | None = None


class WorkspaceResponse(BaseModel):
  id: UUID
  name: str
  slug: str
  is_active: bool
  created_at: datetime
  updated_at: datetime


class OrganizationContextResponse(BaseModel):
  workspace: WorkspaceResponse
  role: str
  permissions: list[str]
