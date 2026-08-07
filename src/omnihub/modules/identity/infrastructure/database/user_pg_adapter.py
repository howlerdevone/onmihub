from __future__ import annotations

from omnihub.common import PgClient
from omnihub.modules.identity.domain.entities import User
from omnihub.modules.identity.ports.user_identity_provider_port import UserIdentityProviderPort


class UserPgIdentityAdapter(UserIdentityProviderPort):
  def __init__(self, db: PgClient):
    self.db = db

  async def create_user(self, user: User) -> User:
    """
    Create a new user in the database.
    """
    row = await self.db.fetchrow(
      """
      INSERT INTO identity.users (id, email, display_name, preferred_language, timezone)
      VALUES ($1, $2, $3, $4, $5)
      RETURNING id, email, display_name, preferred_language, timezone
      """,
      user.id,
      user.email,
      user.display_name,
      user.preferred_language,
      user.timezone,
    )
    if not row:
      raise RuntimeError("Failed to create user in identity.users")
    return User(
      id=row["id"],
      email=row["email"],
      display_name=row["display_name"],
      preferred_language=row["preferred_language"],
      timezone=row["timezone"],
    )

  async def get_user_by_email(self, email: str | None) -> User | None:
    """
    Retrieve a user from the database by their email address.
    Returns None if no user is found.
    """
    row = await self.db.fetchrow("SELECT * FROM identity.users WHERE email = $1", email)
    if not row:
      return None
    return User(
      id=row["id"],
      email=row["email"],
      display_name=row["display_name"],
      preferred_language=row["preferred_language"],
      timezone=row["timezone"],
    )
