import contextlib
from collections.abc import AsyncIterator
from typing import cast

from fastapi import FastAPI

import conduit.api.endpoints.routes as api_endpoints
from conduit.api import errors, tags
from conduit.containers import Container


@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncIterator[None]:
    container = cast(Container, app.extra["container"])
    database = container.db()

    await database.create_database(seed=True)
    yield
    await database.dispose()


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
        container=container,
        **settings.fastapi,
    )

    app.include_router(api_endpoints.router)

    errors.register_error_handlers(app)

    return app


app = create_app()
