from __future__ import annotations

from typing import Protocol

from omnihub.modules.catalog.domain.entities import Area


class AreaProviderPort(Protocol):
  """Architectural port defining area read operations."""

  async def get_all_areas(self) -> list[Area]:
    """Fetch all available areas."""
    ...
