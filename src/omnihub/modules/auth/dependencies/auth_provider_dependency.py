from fastapi import Depends, Request

from omnihub.common.db.pg_client import PgClient
from omnihub.modules.auth.application.service import AuthApplicationService
from omnihub.modules.auth.infrastructure.supabase.auth_supabase_adapter import SupabaseAuthAdapter
from omnihub.modules.auth.ports.auth_provider_port import AuthProviderPort
from omnihub.modules.identity.application.service import IdentityApplicationService
from omnihub.modules.identity.infrastructure.database.user_pg_adapter import UserPgIdentityAdapter


async def get_identity_service(request: Request) -> IdentityApplicationService:
  """Dependency factory providing the identity context wireframe."""
  db_client: PgClient = request.state.db_client
  adapter = UserPgIdentityAdapter(db=db_client)
  return IdentityApplicationService(user_identity_provider=adapter)


async def get_auth_provider(request: Request) -> AuthProviderPort:
  """Return the configured authentication provider adapter."""
  client = request.app.state.supabase_client
  return SupabaseAuthAdapter(client=client)


async def get_auth_service(
  auth_provider: AuthProviderPort = Depends(get_auth_provider),
  identity_service: IdentityApplicationService = Depends(get_identity_service),
) -> AuthApplicationService:
  """Composition root for authentication workflows."""
  return AuthApplicationService(
    auth_provider=auth_provider,
    identity_service=identity_service,
  )