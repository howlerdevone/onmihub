from __future__ import annotations

from typing import Protocol

from omnihub.modules.identity.domain.entities import User


class UserIdentityProviderPort(Protocol):
    """
    Architectural Port defining strict capabilities required from any external Identity Provider
    (IdP) like Supabase, Clerk, or Auth0.
    """

    async def create_user(self, user: User) -> User:
        """
        Create a new user in the external Identity Provider with the provided user details.
        """
        ...

    async def get_user_by_email(self, email: str | None) -> User | None:
        """
        Retrieve a user from the external Identity Provider by their email address.
        Returns None if no user is found.
        """
        ...
