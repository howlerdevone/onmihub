from omnihub.modules.auth.domain.entities import AuthSession
from omnihub.modules.auth.infrastructure.http.schemas import RegistrationRequest
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
      # Atomically provision local tables and default Tenant Workspace container boundaries
      user = await self.identity_service.create_user(User(
        id=auth_session.user_id,
        email=email,
        refresh_token=auth_session.refresh_token,
        access_token=auth_session.access_token,
        display_name=None,
        preferred_language=None,
        timezone=None
      ))
        
    return auth_session, user

  async def execute_registration_flow(self, data: RegistrationRequest) -> tuple[AuthSession, User | None]:
    """
    Orchestrates user registration via the abstract provider port 
    and synchronizes multi-tenant database state boundaries.
    """

    auth_session = await self.auth_provider.create_user_with_credentials(data.email, data.password)
    user = None

    if auth_session:
      user = await self.identity_service.create_user(User(
        id=auth_session.user_id,
        email=data.email,
        refresh_token=auth_session.refresh_token,
        access_token=auth_session.access_token,
        display_name=data.display_name,
        preferred_language=data.preferred_language,
        timezone=data.timezone
      ))
    
    return auth_session, user