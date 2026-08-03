from __future__ import annotations

from uuid import UUID

from supabase import Client

from omnihub.common.time import parse_timestamp
from omnihub.modules.auth.domain.entities import AuthSession
from omnihub.modules.auth.domain.exceptions import AuthError, InvalidCredentialsError, UserAlreadyExistsError
from omnihub.modules.auth.ports.auth_provider_port import AuthProviderPort


class SupabaseAuthAdapter(AuthProviderPort):
    """
    Concrete infrastructure adapter wrapping the official Supabase Python SDK.
    Plugs seamlessly into the AuthProviderPort contract.
    """

    def __init__(self, client: Client) -> None:
        self.client = client

    async def authenticate_with_password(self, email: str, password: str) -> AuthSession:
        """
        Authenticate user with email and password via Supabase.
        Translates native Supabase response into our clean, agnostic AuthSession domain object.
        """
        auth_response = self.client.auth.sign_in_with_password({"email": email, "password": password})

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
            expires_at=parse_timestamp(session.expires_at),
        )

    async def create_user_with_credentials(self, email: str, password: str) -> AuthSession:
        """
        Create a new user in Supabase with email and password.
        Returns an AuthSession for the newly created user.
        """
        try:
            auth_response = self.client.auth.sign_up({"email": email, "password": password})
        except Exception as error:
            error_code = self._extract_error_code(error)
            if error_code in {"user_already_exists", "email_exists", "identity_already_exists"}:
                raise UserAlreadyExistsError("User already exists") from error
            raise AuthError("Failed to create user.") from error

        session = auth_response.session
        user = auth_response.user

        if not session or not user:
            raise AuthError("Failed to create user.")

        return AuthSession(
            id=UUID(user.id),
            user_id=UUID(user.id),
            access_token=session.access_token,
            refresh_token=session.refresh_token,
            expires_at=parse_timestamp(session.expires_at),
        )

    @staticmethod
    def _extract_error_code(error: Exception) -> str | None:
        """Extract a Supabase auth error code/name without depending on SDK internals."""
        code = getattr(error, "code", None)
        if isinstance(code, str) and code:
            return code
        name = getattr(error, "name", None)
        if isinstance(name, str) and name:
            return name
        return None
