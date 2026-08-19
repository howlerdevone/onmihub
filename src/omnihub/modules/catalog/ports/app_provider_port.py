from __future__ import annotations

from typing import Protocol

from omnihub.modules.catalog.domain.entities import App


class AppProviderPort(Protocol):
  """Architectural port defining app read operations."""

  async def get_all_apps(self) -> list[App]:
    """Fetch all available apps."""
    ...

  async def get_apps_by_area(self, area_id: str) -> list[App]:
    """Fetch all apps belonging to a specific area."""
    ...
