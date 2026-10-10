from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import EmailStr

from omnihub.common import CustomBaseModel


class RegisterUserRequest(CustomBaseModel):
  email: EmailStr
  workspace_name: str


class RegisterUserResponse(CustomBaseModel):
  user_id: UUID
  workspace_id: UUID


class UserResponse(CustomBaseModel):
  id: UUID
  email: str
  firstname: str | None = None
  lastname: str | None = None
  preferred_language: str | None = None
  timezone: str | None = None
  onboarding_completed_at: datetime | None = None
