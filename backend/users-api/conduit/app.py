import contextlib
from collections.abc import AsyncIterator
from typing import cast

from fastapi import FastAPI

import conduit.api.routes as api_endpoints
from conduit.api.errors import handlers
from conduit.api.openapi import tags
from conduit.containers import Container


@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncIterator[None]:
    container = cast(Container, app.extra["container"])
    database = container.db()

    await database.create_database()
    yield
    await database.dispose()


def create_app(container: Container) -> FastAPI:
    """Creates the FastAPI application."""

    settings = container.app_settings()
    app = FastAPI(
        title="Conduit Users API",
        summary="Users REST API implemented with FastAPI framework.",
        description="Inspirational link: [Realworld GitHub](https://github.com/gothinkster/realworld).",
        version="0.1.0",
        lifespan=app_lifespan,
        docs_url="/",
        openapi_tags=tags.tags_metadata(),
        redoc_url=None,  # Disable ReDoc documentaion
        container=container,
        **settings.fastapi,
    )

    app.include_router(api_endpoints.router)

    handlers.register_error_handlers(app)

    return app


def build_app() -> FastAPI:
    container = Container()
    return create_app(container)


app = build_app()
