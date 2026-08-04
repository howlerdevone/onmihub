class IdentityError(Exception):
  """Base class for identity domain errors."""


class UserAlreadyExistsError(IdentityError):
  """Raised when attempting to create a user that already exists."""
