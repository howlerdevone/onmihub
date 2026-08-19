from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from omnihub.modules.auth.dependencies import get_authenticated_user_id
from omnihub.modules.catalog.application.service import CatalogApplicationService
from omnihub.modules.catalog.dependencies.catalog_dependency import get_catalog_service
from omnihub.modules.catalog.infrastructure.http.schemas import AppResponse, AreaResponse


router = APIRouter(prefix="/v1/catalog", tags=["Catalog Operations"])


@router.get("/areas", response_model=list[AreaResponse], status_code=status.HTTP_200_OK)
async def get_all_areas(
  _=Depends(get_authenticated_user_id),
  service: CatalogApplicationService = Depends(get_catalog_service),
):
  """Fetch all available areas."""
  try:
    areas = await service.get_all_areas()
    return [AreaResponse(id=area.id, name=area.name) for area in areas]
  except Exception as error:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail={
        "message": "Catalog gateway error. Please contact support.",
        "code": "SYSTEM_ERROR",
      },
    ) from error


@router.get("/areas/{area_id}/apps", response_model=list[AppResponse], status_code=status.HTTP_200_OK)
async def get_apps_by_area(
  area_id: str,
  _=Depends(get_authenticated_user_id),
  service: CatalogApplicationService = Depends(get_catalog_service),
):
  """Fetch all apps belonging to a specific area."""
  try:
    apps = await service.get_apps_by_area(area_id)
    return [
      AppResponse(
        id=app.id,
        name=app.name,
        description=app.description,
        icon_url=app.icon_url,
        url=app.url,
      )
      for app in apps
    ]
  except Exception as error:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail={
        "message": "Catalog gateway error. Please contact support.",
        "code": "SYSTEM_ERROR",
      },
    ) from error


@router.get("/apps", response_model=list[AppResponse], status_code=status.HTTP_200_OK)
async def get_all_apps(
  _=Depends(get_authenticated_user_id),
  service: CatalogApplicationService = Depends(get_catalog_service),
):
  """Fetch all available apps."""
  try:
    apps = await service.get_all_apps()
    return [
      AppResponse(
        id=app.id,
        name=app.name,
        description=app.description,
        icon_url=app.icon_url,
        url=app.url,
      )
      for app in apps
    ]
  except Exception as error:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail={
        "message": "Catalog gateway error. Please contact support.",
        "code": "SYSTEM_ERROR",
      },
    ) from error
