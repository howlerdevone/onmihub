from __future__ import annotations

from fastapi import Request

from omnihub.modules.catalog.application.service import CatalogApplicationService
from omnihub.modules.catalog.infrastructure.database.app_pg_adapter import AppPgAdapter
from omnihub.modules.catalog.infrastructure.database.area_pg_adapter import AreaPgAdapter


async def get_catalog_service(request: Request) -> CatalogApplicationService:
  """Inject the catalog application service with initialized adapters."""
  db_client = request.app.state.db_client
  area_adapter = AreaPgAdapter(db_client)
  app_adapter = AppPgAdapter(db_client)
  return CatalogApplicationService(area_provider=area_adapter, app_provider=app_adapter)
