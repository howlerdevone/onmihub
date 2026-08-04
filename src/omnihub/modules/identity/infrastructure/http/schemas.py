from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, EmailStr


class RegisterUserRequest(BaseModel):
  email: EmailStr
  workspace_name: str


class RegisterUserResponse(BaseModel):
  user_id: UUID
  workspace_id: UUID
