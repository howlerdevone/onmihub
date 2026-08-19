class CatalogError(Exception):
  """Base class for catalog domain errors."""


class AreaNotFoundError(CatalogError):
  """Raised when an area does not exist."""
