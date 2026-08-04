class OrganizationError(Exception):
  """Base class for organization domain errors."""


class OrganizationAlreadyExistsError(OrganizationError):
  """Raised when attempting to create a workspace with an existing slug."""


class OrganizationNotFoundError(OrganizationError):
  """Raised when the workspace does not exist."""


class OrganizationAccessDeniedError(OrganizationError):
  """Raised when user is not a member of the workspace."""
