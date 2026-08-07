from __future__ import annotations

from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from omnihub.modules.auth.dependencies.auth_provider_dependency import get_auth_provider
from omnihub.modules.auth.domain.exceptions import AuthError
from omnihub.modules.auth.ports.auth_provider_port import AuthProviderPort


bearer_scheme = HTTPBearer(auto_error=True)


async def get_current_user_token(
  credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str:
  """Return the current authenticated bearer token."""
  return credentials.credentials


async def get_authenticated_user_id(
  token: str = Depends(get_current_user_token),
  auth_provider: AuthProviderPort = Depends(get_auth_provider),
) -> UUID:
  """Validate auth token via provider and return authenticated user id."""

  try:
    return await auth_provider.validate_token_and_get_user_id(token)
  except AuthError as error:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail={
        "message": str(error),
        "code": "AUTH_INVALID_TOKEN",
      },
    ) from error
