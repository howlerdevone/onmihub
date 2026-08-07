from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from omnihub.modules.auth.infrastructure.http.schemas import RegistrationRequest
from omnihub.modules.identity.domain.entities import User


@dataclass(frozen=True)
class RegistrationInput:
  email: str
  password: str
  display_name: str | None = None
  preferred_language: str | None = None
  timezone: str | None = None


def map_registration_request(payload: RegistrationRequest) -> RegistrationInput:
  return RegistrationInput(
    email=str(payload.email),
    password=payload.password,
    display_name=payload.display_name,
    preferred_language=payload.preferred_language,
    timezone=payload.timezone,
  )


def map_login_user(
  *,
  user_id: UUID,
  email: str,
) -> User:
  return User(
    id=user_id,
    email=email,
    display_name=None,
    preferred_language=None,
    timezone=None,
  )


def map_registration_user(
  *,
  user_id: UUID,
  data: RegistrationInput,
) -> User:
  return User(
    id=user_id,
    email=data.email,
    display_name=data.display_name,
    preferred_language=data.preferred_language,
    timezone=data.timezone,
  )
