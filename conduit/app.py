import contextlib
from typing import AsyncIterator, cast

from fastapi import FastAPI

import conduit.api.endpoints.routes as api_endpoints
import conduit.api.errors as errors
from conduit.api import tags
from conduit.containers import Container


@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncIterator[None]:
    container = cast(Container, app.extra["container"])
    database = container.db()
    await database.create_tables()
    yield


def create_app() -> FastAPI:
    """Creates the FastAPI application."""

    container = Container()

    settings = container.app_settings()
    app = FastAPI(
        title="Conduit Realworld REST API",
        summary="Implementation of Conduit Realworld API using FastAPI.",
        description="Inspirational link: [Realworld GitHub](https://github.com/gothinkster/realworld)",
        version="0.1.0",
        lifespan=app_lifespan,
        docs_url="/",
        openapi_tags=tags.open_api_tags_metadata(),
        redoc_url=None,  # Disable ReDoc documentaion
        **settings.fastapi,
        container=container,
    )

    app.include_router(api_endpoints.router)

    errors.register_error_handlers(app)

    return app


app = create_app()
