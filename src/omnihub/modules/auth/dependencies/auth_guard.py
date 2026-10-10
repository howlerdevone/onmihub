from __future__ import annotations

from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from omnihub.modules.auth.dependencies.auth_provider_dependency import get_auth_provider
from omnihub.modules.auth.domain.exceptions import AuthError
from omnihub.modules.auth.ports.auth_provider_port import AuthProviderPort


bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user_token(
  credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
  """
  Return the current authenticated bearer token.

  Uses auto_error=False so a missing or malformed Authorization header raises
  401 instead of FastAPI's default 403, keeping every unauthenticated outcome
  on the same status code for clients driving token refresh.
  """
  if credentials is None or not credentials.credentials:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail={
        "message": "Missing bearer token.",
        "code": "AUTH_MISSING_TOKEN",
      },
      headers={"WWW-Authenticate": "Bearer"},
    )
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
      headers={"WWW-Authenticate": "Bearer"},
    ) from error
