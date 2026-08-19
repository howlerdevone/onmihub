from __future__ import annotations

from omnihub.modules.catalog.domain.entities import App, Area
from omnihub.modules.catalog.ports.app_provider_port import AppProviderPort
from omnihub.modules.catalog.ports.area_provider_port import AreaProviderPort


class CatalogApplicationService:
  """Application service orchestrating catalog read operations."""

  def __init__(self, area_provider: AreaProviderPort, app_provider: AppProviderPort) -> None:
    self.area_provider = area_provider
    self.app_provider = app_provider

  async def get_all_areas(self) -> list[Area]:
    """Fetch all available areas."""
    return await self.area_provider.get_all_areas()

  async def get_all_apps(self) -> list[App]:
    """Fetch all available apps."""
    return await self.app_provider.get_all_apps()

  async def get_apps_by_area(self, area_id: str) -> list[App]:
    """Fetch all apps belonging to a specific area."""
    return await self.app_provider.get_apps_by_area(area_id)
