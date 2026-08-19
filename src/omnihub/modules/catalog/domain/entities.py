from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Area:
  """Represents a category of applications."""

  id: str
  name: str


@dataclass
class App:
  """Represents an application in the catalog."""

  id: str
  name: str
  description: str | None
  icon_url: str | None
  url: str | None
