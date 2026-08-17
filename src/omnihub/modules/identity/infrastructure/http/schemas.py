from __future__ import annotations

from uuid import UUID

from pydantic import EmailStr

from omnihub.common import CustomBaseModel


class RegisterUserRequest(CustomBaseModel):
  email: EmailStr
  workspace_name: str


class RegisterUserResponse(CustomBaseModel):
  user_id: UUID
  workspace_id: UUID
