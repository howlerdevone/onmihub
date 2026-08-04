from abc import ABC, abstractmethod
from uuid import UUID

from omnihub.modules.auth.domain.entities import AuthSession


class AuthProviderPort(ABC):
  """
  Architectural Port defining strict capabilities required from any
  external Identity Provider (IdP) like Supabase, Clerk, or Auth0.
  """

  @abstractmethod
  async def authenticate_with_password(self, email: str, password: str) -> AuthSession:
    """Verify user credentials against the remote Identity Provider provider."""
    pass

  @abstractmethod
  async def create_user_with_credentials(self, email: str, password: str) -> AuthSession:
    """Create a new user in the remote Identity Provider with email and password."""
    pass

  @abstractmethod
  async def refresh_session(self, refresh_token: str) -> AuthSession:
    """Exchange a refresh token for a new authenticated session."""
    pass

  @abstractmethod
  async def validate_token_and_get_user_id(self, token: str) -> UUID:
    """Validate an access token and return the authenticated user id."""
    pass
