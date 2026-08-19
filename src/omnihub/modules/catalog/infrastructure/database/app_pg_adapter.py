from __future__ import annotations

from omnihub.common.db.pg_client import PgClient
from omnihub.modules.catalog.domain.entities import App
from omnihub.modules.catalog.ports.app_provider_port import AppProviderPort


class AppPgAdapter(AppProviderPort):
  """PostgreSQL implementation of the catalog app port."""

  def __init__(self, db: PgClient):
    self.db = db

  async def get_all_apps(self) -> list[App]:
    """Fetch all available apps."""
    rows = await self.db.fetch(
      """
      SELECT id, name, description, icon_url, url
      FROM catalog.apps
      ORDER BY name ASC
      """
    )
    return [
      App(
        id=str(row["id"]),
        name=row["name"],
        description=row["description"],
        icon_url=row["icon_url"],
        url=row["url"],
      )
      for row in rows
    ]

  async def get_apps_by_area(self, area_id: str) -> list[App]:
    """Fetch all apps belonging to a specific area."""
    rows = await self.db.fetch(
      """
      SELECT a.id, a.name, a.description, a.icon_url, a.url
      FROM catalog.apps a
      INNER JOIN catalog.app_areas aa ON a.id = aa.app_id
      WHERE aa.area_id = $1
      ORDER BY a.name ASC
      """,
      area_id,
    )
    return [
      App(
        id=str(row["id"]),
        name=row["name"],
        description=row["description"],
        icon_url=row["icon_url"],
        url=row["url"],
      )
      for row in rows
    ]
