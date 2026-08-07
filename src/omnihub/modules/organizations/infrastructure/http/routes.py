from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from omnihub.modules.auth.dependencies import get_authenticated_user_id
from omnihub.modules.organizations.application.service import OrganizationsApplicationService
from omnihub.modules.organizations.dependencies.workspace_dependency import get_organizations_service
from omnihub.modules.organizations.domain.exceptions import (
  OrganizationAccessDeniedError,
  OrganizationAlreadyExistsError,
  OrganizationNotFoundError,
)
from omnihub.modules.organizations.infrastructure.http.schemas import (
  CreateWorkspaceRequest,
  OrganizationContextResponse,
  WorkspaceResponse,
)


router = APIRouter(prefix="/v1/organizations", tags=["Organization Operations"])


@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
  payload: CreateWorkspaceRequest,
  current_user_id: UUID = Depends(get_authenticated_user_id),
  service: OrganizationsApplicationService = Depends(get_organizations_service),
):
  """Create a private workspace for the current user."""
  try:
    workspace = await service.create_workspace(
      user_id=current_user_id,
      name=payload.name,
      slug=payload.slug,
    )
    return WorkspaceResponse(
      id=workspace.id,
      name=workspace.name,
      slug=workspace.slug,
      is_active=workspace.is_active,
      created_at=workspace.created_at,
      updated_at=workspace.updated_at,
    )
  except OrganizationAlreadyExistsError:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail={
        "message": "Workspace with this slug already exists.",
        "code": "ORG_ALREADY_EXISTS",
      },
    ) from None
  except Exception as error:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail={
        "message": "Organization gateway error. Please contact support.",
        "code": "SYSTEM_ERROR",
      },
    ) from error


@router.get("/{workspace_id}", response_model=OrganizationContextResponse, status_code=status.HTTP_200_OK)
async def get_workspace(
  workspace_id: UUID,
  current_user_id: UUID = Depends(get_authenticated_user_id),
  service: OrganizationsApplicationService = Depends(get_organizations_service),
):
  """Return workspace context and default permissions for the current user."""
  try:
    context = await service.get_workspace(workspace_id=workspace_id, user_id=current_user_id)
    return OrganizationContextResponse(
      workspace=WorkspaceResponse(
        id=context.workspace.id,
        name=context.workspace.name,
        slug=context.workspace.slug,
        is_active=context.workspace.is_active,
        created_at=context.workspace.created_at,
        updated_at=context.workspace.updated_at,
      ),
      role=context.role,
      permissions=context.permissions,
    )
  except OrganizationNotFoundError:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail={
        "message": "Workspace not found.",
        "code": "ORG_NOT_FOUND",
      },
    ) from None
  except OrganizationAccessDeniedError:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail={
        "message": "Access denied to workspace.",
        "code": "ORG_ACCESS_DENIED",
      },
    ) from None
  except Exception as error:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail={
        "message": "Organization gateway error. Please contact support.",
        "code": "SYSTEM_ERROR",
      },
    ) from error
