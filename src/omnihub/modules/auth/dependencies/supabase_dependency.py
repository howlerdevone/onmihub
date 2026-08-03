from fastapi import Depends, Request

from omnihub.common.db.pg_client import PgClient
from omnihub.gateway.supabase import get_supabase_client
from omnihub.modules.auth.application.service import AuthApplicationService

# Core architectural layers
from omnihub.modules.auth.infrastructure.supabase.auth_supabase_adapter import SupabaseAuthAdapter
from omnihub.modules.identity.application.service import IdentityApplicationService
from omnihub.modules.identity.infrastructure.database.user_pg_adapter import UserPgIdentityAdapter


async def get_identity_service(request: Request) -> IdentityApplicationService:
    """Dependency factory providing the identity context wireframe."""
    db_client: PgClient = request.state.db_client
    adapter = UserPgIdentityAdapter(db=db_client)
    return IdentityApplicationService(user_identity_provider=adapter)


async def get_auth_service(
    request: Request, identity_service: IdentityApplicationService = Depends(get_identity_service)
) -> AuthApplicationService:
    """
    Centralized Composition Root. Instantiates the explicit Supabase adapter
    over the generic abstract Port and injects it into the application layer.

    if you switch to a different identity provider (e.g., Clerk), you would only need to replace
    the adapter here without touching the application service.
    """
    # 1. Instantiate the Supabase client lazily so missing env vars raise a
    # clear error at the dependency creation point rather than during import.
    try:
        client = get_supabase_client()
    except RuntimeError as exc:
        # Re-raise with context so the server logs are explicit about missing config
        raise RuntimeError("Supabase configuration error: " + str(exc)) from exc

    # 2. Instantiate the explicit infrastructure adapter plugging it into the generic Port
    auth_provider_adapter = SupabaseAuthAdapter(client=client)

    # 3. Wire up the decoupled application container and return it
    return AuthApplicationService(
        auth_provider=auth_provider_adapter,
        identity_service=identity_service,
    )
