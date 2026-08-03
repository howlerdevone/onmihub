from __future__ import annotations

from omnihub.modules.identity.domain.entities import User
from omnihub.modules.identity.domain.exceptions import UserAlreadyExistsError
from omnihub.modules.identity.ports.user_identity_provider_port import UserIdentityProviderPort


class IdentityApplicationService:
  def __init__(self, user_identity_provider: UserIdentityProviderPort) -> None:
    self.user_identity_provider = user_identity_provider

  async def get_user_by_email(self, email: str | None) -> User | None:
    return await self.user_identity_provider.get_user_by_email(email)

  async def create_user(self, user: User) -> User:
    existing_user = await self.user_identity_provider.get_user_by_email(user.email)
    if existing_user:
      raise UserAlreadyExistsError(f"User with email {user.email} already exists.")
    return await self.user_identity_provider.create_user(user)
  