from fastapi import FastAPI

import conduit.api.endpoints as api_endpoints
from conduit.api.settings import get_settings


def create_app() -> FastAPI:
    """Creates the FastAPI application."""

    settings = get_settings()

    app = FastAPI(**settings.fastapi_settings)

    app.include_router(api_endpoints.router)

    return app


app = create_app()
