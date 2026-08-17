from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from omnihub.modules.identity.domain.entities import User
from omnihub.modules.auth.infrastructure.http.schemas import RegistrationRequest


@dataclass(frozen=True)
class RegistrationInput:
  email: str
  password: str
  firstname: str | None = None
  lastname: str | None = None
  preferred_language: str | None = None
  timezone: str | None = None


def map_registration_request(payload: RegistrationRequest) -> RegistrationInput:
  return RegistrationInput(
    email=str(payload.email),
    password=payload.password,
    firstname=payload.firstname,
    lastname=payload.lastname,
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
    firstname=None,
    lastname=None,
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
    firstname=data.firstname,
    lastname=data.lastname,
    preferred_language=data.preferred_language,
    timezone=data.timezone,
  )
