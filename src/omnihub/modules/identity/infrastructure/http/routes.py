from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from omnihub.modules.auth.dependencies import get_authenticated_user_id, get_identity_service
from omnihub.modules.identity.application.service import IdentityApplicationService
from omnihub.modules.identity.infrastructure.http.schemas import UserResponse


router = APIRouter(prefix="/v1/users", tags=["Users"])


@router.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
  return {"status": "ok"}


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_current_user(
  current_user_id: UUID = Depends(get_authenticated_user_id),
  service: IdentityApplicationService = Depends(get_identity_service),
):
  """Get the current authenticated user's profile."""
  try:
    user = await service.get_user(user_id=current_user_id)
    if not user:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
          "message": "User not found.",
          "code": "USER_NOT_FOUND",
        },
      )
    return UserResponse(
      id=user.id,
      email=user.email,
      firstname=user.firstname,
      lastname=user.lastname,
      preferred_language=user.preferred_language,
      timezone=user.timezone,
      onboarding_completed_at=user.onboarding_completed_at,
    )
  except HTTPException:
    raise
  except Exception as error:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail={
        "message": "Failed to retrieve user profile.",
        "code": "USER_PROFILE_ERROR",
      },
    ) from error
