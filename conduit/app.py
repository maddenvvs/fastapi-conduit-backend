from fastapi import FastAPI

import conduit.api.endpoints as api_endpoints
from conduit.api.settings import get_settings


def create_app() -> FastAPI:
    """Creates the FastAPI application."""

    settings = get_settings()

    application = FastAPI(**settings.fastapi_settings)

    application.include_router(api_endpoints.router)

    return application


app = create_app()
