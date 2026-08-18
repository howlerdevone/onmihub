class AuthError(Exception):
  """Base class for authentication errors."""


class InvalidCredentialsError(AuthError):
  """Raised when credentials are missing or invalid."""


class SessionExpiredError(AuthError):
  """Raised when an authentication session is no longer valid."""


class UserAlreadyExistsError(AuthError):
  """Raised when trying to register a user that already exists."""


class EmailNotConfirmedError(AuthError):
  """Raised when a user's email has not been confirmed yet."""
