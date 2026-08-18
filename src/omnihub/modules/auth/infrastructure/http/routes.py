from fastapi import APIRouter, Depends, HTTPException, status

from omnihub.modules.auth.application.service import AuthApplicationService
from omnihub.modules.auth.dependencies.auth_provider_dependency import get_auth_service
from omnihub.modules.auth.domain.exceptions import (
  AuthError,
  EmailNotConfirmedError,
  InvalidCredentialsError,
  UserAlreadyExistsError,
)
from omnihub.modules.auth.infrastructure.http.mappers import map_registration_request
from omnihub.modules.auth.infrastructure.http.schemas import (
  AuthUserResponse,
  LoginRequest,
  LoginResponse,
  RefreshSessionRequest,
  RefreshSessionResponse,
  RegistrationRequest,
  RegistrationResponse,
)


router = APIRouter(prefix="/v1/auth", tags=["Authentication Operations"])


@router.get("/health")
async def health_check() -> dict[str, str]:
  return {"status": "ok"}


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login_gateway(payload: LoginRequest, auth_service: AuthApplicationService = Depends(get_auth_service)):
  """
  HTTP proxy gateway executing centralized platform authentication.
  100% decoupled from third-party vendor SDK signatures.
  """

  try:
    session, user = await auth_service.execute_login_flow(email=payload.email, password=payload.password)

    return LoginResponse(
      status="success",
      access_token=session.access_token,
      refresh_token=session.refresh_token,
      expires_at=session.expires_at,
      user=AuthUserResponse.model_validate(user) if user else None,
    )

  except InvalidCredentialsError:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail={"message": "The provided email or password is incorrect", "code": "AUTH_INVALID_CREDENTIALS"},
    ) from None

  except UserAlreadyExistsError:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail={"message": "A user with this email already exists.", "code": "AUTH_USER_ALREADY_EXISTS"},
    ) from None

  except EmailNotConfirmedError:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail={"message": "Email not confirmed. Please check your inbox.", "code": "AUTH_EMAIL_NOT_CONFIRMED"},
    ) from None

  except Exception as error:
    print(f"Unexpected error during login: {error}")
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail={"message": "Authentication error. Please try again.", "code": "AUTH_ERROR"},
    ) from None


@router.post("/register", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register_gateway(
  payload: RegistrationRequest, auth_service: AuthApplicationService = Depends(get_auth_service)
):
  """HTTP proxy gateway executing centralized platform registration."""

  try:
    data = map_registration_request(payload)
    session, user = await auth_service.execute_registration_flow(data)

    return RegistrationResponse(
      status="success",
      access_token=session.access_token,
      refresh_token=session.refresh_token,
      expires_at=session.expires_at,
      user=AuthUserResponse.model_validate(user) if user else None,
    )

  except InvalidCredentialsError:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail={"message": "The provided email or password is incorrect", "code": "AUTH_INVALID_CREDENTIALS"},
    ) from None

  except UserAlreadyExistsError:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail={"message": "A user with this email already exists.", "code": "AUTH_USER_ALREADY_EXISTS"},
    ) from None

  except Exception:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail={"message": "Registration failed. Please try again.", "code": "AUTH_ERROR"},
    ) from None


@router.post("/refresh", response_model=RefreshSessionResponse, status_code=status.HTTP_200_OK)
async def refresh_gateway(
  payload: RefreshSessionRequest, auth_service: AuthApplicationService = Depends(get_auth_service)
):
  """Exchange a refresh token for a new access token and session metadata."""
  try:
    session = await auth_service.execute_refresh_flow(payload.refresh_token)

    return RefreshSessionResponse(
      status="success",
      access_token=session.access_token,
      refresh_token=session.refresh_token,
      expires_at=session.expires_at,
    )

  except AuthError:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail={"message": "The provided refresh token is invalid.", "code": "AUTH_INVALID_TOKEN"},
    ) from None

  except Exception:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail={"message": "Token refresh failed. Please try again.", "code": "AUTH_ERROR"},
    ) from None
