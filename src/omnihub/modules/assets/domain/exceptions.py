from __future__ import annotations


class FileError(Exception):
  """Base class for file domain errors."""


class FileAlreadyExistsError(FileError):
  """Raised when attempting to create a file that already exists."""


class FileNotFoundError(FileError):
  """Raised when the requested file does not exist."""
