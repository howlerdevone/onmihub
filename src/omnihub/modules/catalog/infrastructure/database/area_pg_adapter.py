from __future__ import annotations

from omnihub.common.db.pg_client import PgClient
from omnihub.modules.catalog.domain.entities import Area
from omnihub.modules.catalog.ports.area_provider_port import AreaProviderPort


class AreaPgAdapter(AreaProviderPort):
  """PostgreSQL implementation of the catalog area port."""

  def __init__(self, db: PgClient):
    self.db = db

  async def get_all_areas(self) -> list[Area]:
    """Fetch all available areas."""
    rows = await self.db.fetch(
      """
      SELECT id, name
      FROM catalog.areas
      ORDER BY name ASC
      """
    )
    return [Area(id=row["id"], name=row["name"]) for row in rows]
