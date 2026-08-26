from __future__ import annotations


class StorageError(Exception):
  """Base class for storage domain errors."""


class StorageProvisioningError(StorageError):
  """Raised when a storage folder could not be provisioned."""


class StorageObjectNotFoundError(StorageError):
  """Raised when the requested object does not exist."""
