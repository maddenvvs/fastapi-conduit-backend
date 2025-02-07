import contextlib

from fastapi import FastAPI

import conduit.api.endpoints as api_endpoints
from conduit.api.dependencies import DB_ENGINE
from conduit.api.settings import get_settings
from conduit.persistence.models import create_tables_if_needed


@contextlib.asynccontextmanager
async def app_lifespan(_: FastAPI):
    await create_tables_if_needed(DB_ENGINE)
    yield


def create_app() -> FastAPI:
    """Creates the FastAPI application."""

    settings = get_settings()

    app = FastAPI(
        **settings.fastapi,
        lifespan=app_lifespan,
    )

    app.include_router(api_endpoints.router)

    return app


app = create_app()
