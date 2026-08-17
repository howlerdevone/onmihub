from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import ConfigDict, EmailStr

from omnihub.common import CustomBaseModel


class AuthUserResponse(CustomBaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: UUID
  email: EmailStr
  firstname: str | None = None
  lastname: str | None = None
  preferred_language: str | None = None
  timezone: str | None = None


class LoginRequest(CustomBaseModel):
  """
  Credentials payload forwarded by Next.js frontend to request
  central identity verification via Supabase proxying.
  """

  email: EmailStr
  password: str


class LoginResponse(CustomBaseModel):
  """
  Unified authentication payload returned to Next.js containing
  the active session keys and local multi-tenant profiling metadata.
  """

  status: str
  access_token: str
  refresh_token: str
  expires_at: datetime
  user: AuthUserResponse | None = None


class RefreshSessionRequest(CustomBaseModel):
  refresh_token: str


class RefreshSessionResponse(CustomBaseModel):
  status: str
  access_token: str
  refresh_token: str
  expires_at: datetime


class RegistrationRequest(CustomBaseModel):
  """
  Credentials payload forwarded by frontend to request
  central identity registration via third party proxying.
  """

  email: EmailStr
  password: str
  firstname: str | None = None
  lastname: str | None = None
  timezone: str | None = None
  birthdate: str | None = None
  preferred_language: str | None = None


class RegistrationResponse(CustomBaseModel):
  """
  Unified authentication payload returned to frontend containing
  the active session keys and local multi-tenant profiling metadata.
  """

  status: str
  access_token: str
  refresh_token: str
  expires_at: datetime
  user: AuthUserResponse | None = None
