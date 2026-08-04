from __future__ import annotations

import re


def slugify(value: str) -> str:
  """Convert arbitrary text into a URL-safe slug."""
  slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
  return slug or "workspace"
