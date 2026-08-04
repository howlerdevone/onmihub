"""Utilities for handling timestamp conversions and parsing."""

from datetime import UTC, datetime
from typing import Optional, Union


def parse_timestamp(timestamp: int | float | str | None) -> datetime:
  """Convert Unix timestamp or ISO format string to datetime.

  Args:
      timestamp: Can be a Unix timestamp (int/float), ISO format string, or None.

  Returns:
      A datetime object.

  Raises:
      ValueError: If the timestamp is None or format is unrecognized.
  """
  if timestamp is None:
    raise ValueError("Timestamp cannot be None")
  if isinstance(timestamp, (int, float)):
    return datetime.fromtimestamp(timestamp, UTC)

  parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
  if parsed.tzinfo is None:
    return parsed.replace(tzinfo=UTC)
  return parsed.astimezone(UTC)
