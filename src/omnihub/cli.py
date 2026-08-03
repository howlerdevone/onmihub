import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .common.logging import setup_logging
from .gateway.database import database_lifespan, inject_db_connection_middleware
from .gateway.router import get_central_application_router

# Initialize logging for the application
setup_logging()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(
        title="Omnihub API Engine",
        description=("Hexagonal, DDD-driven multi-tenant Agentic AI infrastructure orchestrator."),
        version="1.0.0",
        lifespan=database_lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # DB connection middleware
    app.middleware("http")(inject_db_connection_middleware)

    # Register routers
    app.include_router(get_central_application_router())

    return app


# Expose the ASGI app for servers that import the module
application: FastAPI = create_app()


def app(host: str | None = None, port: int | None = None) -> None:
    host = host or os.environ.get("HOST", "127.0.0.1")
    port = int(port or os.environ.get("PORT", "8000"))
    reload_enabled = os.environ.get("OMNIHUB_RELOAD", "false").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }

    uvicorn.run(
        "omnihub.cli:application",
        host=host,
        port=port,
        reload=reload_enabled,
    )
