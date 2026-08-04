from omnihub.modules.auth.domain.entities import AuthSession
from omnihub.modules.auth.infrastructure.http.mappers import RegistrationInput, map_login_user, map_registration_user
from omnihub.modules.auth.ports.auth_provider_port import AuthProviderPort
from omnihub.modules.identity.application.service import IdentityApplicationService
from omnihub.modules.identity.domain.entities import User


class AuthApplicationService:
  """
  Application Service handling central authentication workflows.
  Completely decoupled from specific identity providers implementations.
  """

  def __init__(self, auth_provider: AuthProviderPort, identity_service: IdentityApplicationService):
    self.auth_provider = auth_provider
    self.identity_service = identity_service

  async def execute_login_flow(self, email: str, password: str) -> tuple[AuthSession, User | None]:
    """
    Orchestrates credentials verification via the abstract provider port
    and synchronizes multi-tenant database state boundaries.
    """
    # 1. Delegate credentials check to the active Port (Could be Supabase or Clerk underneath)
    auth_session = await self.auth_provider.authenticate_with_password(email, password)

    # 2. Check local database profile existence through Identity Context
    user = await self.identity_service.get_user_by_email(email)

    if not user and auth_session:
      user = await self.identity_service.create_user(
        map_login_user(
          user_id=auth_session.user_id,
          email=email,
        )
      )

    return auth_session, user

  async def execute_registration_flow(self, data: RegistrationInput) -> tuple[AuthSession, User | None]:
    """
    Orchestrates user registration via the abstract provider port
    and synchronizes multi-tenant database state boundaries.
    """

    auth_session = await self.auth_provider.create_user_with_credentials(data.email, data.password)
    user = None

    if auth_session:
      user = await self.identity_service.create_user(
        map_registration_user(
          user_id=auth_session.user_id,
          data=data,
        )
      )

    return auth_session, user

  async def execute_refresh_flow(self, refresh_token: str) -> AuthSession:
    """Refresh an authenticated session."""
    return await self.auth_provider.refresh_session(refresh_token)
