from abc import ABC, abstractmethod
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