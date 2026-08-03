from __future__ import annotations

from typing import Any

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """
    Credentials payload forwarded by Next.js frontend to request
    central identity verification via Supabase proxying.
    """

    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """
    Unified authentication payload returned to Next.js containing
    the active session keys and local multi-tenant profiling metadata.
    """

    status: str
    access_token: str
    refresh_token: str
    user: dict[str, Any] | None = None  # Optional local multi-tenant profiling metadata


class RegistrationRequest(BaseModel):
    """
    Credentials payload forwarded by frontend to request
    central identity registration via third party proxying.
    """

    email: EmailStr
    password: str
    display_name: str | None = None
    timezone: str | None = None
    birthdate: str | None = None
    preferred_language: str | None = None


class RegistrationResponse(BaseModel):
    """
    Unified authentication payload returned to frontend containing
    the active session keys and local multi-tenant profiling metadata.
    """

    status: str
    access_token: str
    refresh_token: str
    user: dict[str, Any] | None = None  # Optional local multi-tenant profiling metadata
