from fastapi import APIRouter
from omnihub.modules.auth.infrastructure.http.routes import router as auth_router
from omnihub.modules.identity.infrastructure.http.routes import router as identity_router

def get_central_application_router() -> APIRouter:
    """
    Aggregates and exposes all independent context routers from peripheral modules 
    into a unified main application router matrix.
    """
    main_router = APIRouter()
    
    # Register peripheral modular blocks cleanly using the master switchboard
    main_router.include_router(auth_router)
    main_router.include_router(identity_router)
    
    return main_router