from fastapi import APIRouter, HTTPException, status, Depends
from omnihub.modules.auth.application.service import AuthApplicationService
from omnihub.modules.auth.infrastructure.http.schemas import LoginRequest, LoginResponse, RegistrationRequest, RegistrationResponse
from omnihub.modules.auth.dependencies.supabase_dependency import get_auth_service
from omnihub.modules.auth.domain.exceptions import InvalidCredentialsError, UserAlreadyExistsError

router = APIRouter(prefix="/v1/auth", tags=["Authentication Operations"])

@router.get("/health")
async def health_check() -> dict[str, str]:
  return {"status": "ok"}

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login_gateway(
  payload: LoginRequest,
  auth_service: AuthApplicationService = Depends(get_auth_service)
):
  """
  HTTP proxy gateway executing centralized platform authentication.
  100% decoupled from third-party vendor SDK signatures.
  """

  try:
    session, user = await auth_service.execute_login_flow(
      email=payload.email,
      password=payload.password
    )
    
    return LoginResponse(
      status="success",
      access_token=session.access_token,
      refresh_token=session.refresh_token,
      user=user.__dict__ if user else None
    )

  except InvalidCredentialsError:
    # Map business exception into standard explicit HTTP 401 response
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
          "message": "The provided email or password... is incorrect",
          "code": 'AUTH_INVALID_CREDENTIALS'
        }
    )

  except UserAlreadyExistsError:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail={
        "message": "A user with this email already exists.",
        "code": "AUTH_USER_ALREADY_EXISTS"
      }
    )
        
  except Exception as error:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail={
        "message": "Authentication gateway error. Please contact support." + str(error),
        "code": 'SYSTEM ERROR'
      }
    )

@router.post("/register", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register_gateway(
  payload: RegistrationRequest,
  auth_service: AuthApplicationService = Depends(get_auth_service)
):
  """
  HTTP proxy gateway executing centralized platform registration.
  100% decoupled from third-party vendor SDK signatures.
  """

  try:
    session, user = await auth_service.execute_registration_flow(payload)
    
    return RegistrationResponse(
      status="success",
      access_token=session.access_token,
      refresh_token=session.refresh_token,
      user=user.__dict__ if user else None
    )

  except InvalidCredentialsError:
    # Map business exception into standard explicit HTTP 401 response
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
          "message": "The provided email or password is incorrect",
          "code": 'AUTH_INVALID_CREDENTIALS'
        }
    )

  except UserAlreadyExistsError:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail={
        "message": "A user with this email already exists.",
        "code": "AUTH_USER_ALREADY_EXISTS"
      }
    )
        
  except Exception as error:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail={
        "message": "Authentication gateway error. Please contact support." + str(error),
        "code": 'SYSTEM ERROR'
      }
    )