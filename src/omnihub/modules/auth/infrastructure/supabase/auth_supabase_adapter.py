from __future__ import annotations

from uuid import UUID

from supabase import AsyncClient

from omnihub.common.time import parse_timestamp
from omnihub.modules.auth.domain.entities import AuthSession
from omnihub.modules.auth.domain.exceptions import InvalidCredentialsError, AuthError, UserAlreadyExistsError
from omnihub.modules.auth.ports.auth_provider_port import AuthProviderPort


class SupabaseAuthAdapter(AuthProviderPort):
  """
  Concrete infrastructure adapter wrapping the official Supabase Python SDK.
  Plugs seamlessly into the AuthProviderPort contract.
  """

  def __init__(self, client: AsyncClient) -> None:
    self.client = client

  async def authenticate_with_password(self, email: str, password: str) -> AuthSession:
    """
    Authenticate user with email and password via Supabase.
    Translates native Supabase response into our clean, agnostic AuthSession domain object.
    """
    auth_response = await self.client.auth.sign_in_with_password({
      "email": email,
      "password": password,
    })

    session = auth_response.session
    user = auth_response.user

    if not session or not user:
      raise InvalidCredentialsError("Invalid email or password.")

    return AuthSession(
      id=UUID(user.id),
      user_id=UUID(user.id),
      access_token=session.access_token,
      refresh_token=session.refresh_token,
      email=user.email,
      expires_at=parse_timestamp(session.expires_at)
    )

  async def create_user_with_credentials(self, email: str, password: str) -> AuthSession:
    """
    Create a new user in Supabase with email and password.
    Returns an AuthSession for the newly created user.
    """
    auth_response = await self.client.auth.sign_up({
      "email": email,
      "password": password,
    })

    session = auth_response.session
    user = auth_response.user

    if not session or not user:
      raise AuthError("Failed to create user.")

    if user.identities is not None and len(user.identities) == 0:
      raise UserAlreadyExistsError("User already exists.")

    return AuthSession(
      id=UUID(user.id),
      user_id=UUID(user.id),
      access_token=session.access_token,
      refresh_token=session.refresh_token,
      email=user.email,
      expires_at=parse_timestamp(session.expires_at)
    )

  async def refresh_session(self, refresh_token: str) -> AuthSession:
    """Refresh a Supabase session using the provided refresh token."""
    try:
      auth_response = await self.client.auth.refresh_session(refresh_token)
    except Exception as error:
      raise AuthError("Invalid or expired refresh token.") from error

    session = auth_response.session
    user = auth_response.user

    if not session or not user:
      raise AuthError("Failed to refresh session.")

    return AuthSession(
      id=UUID(user.id),
      user_id=UUID(user.id),
      access_token=session.access_token,
      refresh_token=session.refresh_token,
      email=user.email,
      expires_at=parse_timestamp(session.expires_at)
    )

  async def validate_token_and_get_user_id(self, token: str) -> UUID:
    """Validate a bearer token via Supabase and return its subject user id."""
    try:
      auth_response = await self.client.auth.get_user(token)
    except Exception as error:
      raise AuthError("Invalid or expired bearer token.") from error

    user = getattr(auth_response, "user", auth_response)
    user_id = getattr(user, "id", None)

    if not user_id:
      raise AuthError("Invalid or expired bearer token.")

    try:
      return UUID(str(user_id))
    except ValueError as error:
      raise AuthError("Invalid bearer token user identifier.") from error
  