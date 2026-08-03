"""Utilities for handling timestamp conversions and parsing."""

from datetime import datetime


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
        return datetime.fromtimestamp(timestamp)
    else:
        # At this point, type system narrows to str
        return datetime.fromisoformat(timestamp)
