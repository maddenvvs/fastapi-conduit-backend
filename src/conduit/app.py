import contextlib
from typing import AsyncIterator, cast

from fastapi import FastAPI

import conduit.api.endpoints as api_endpoints
import conduit.api.errors as errors
from conduit.containers import Container


@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncIterator[None]:
    container = cast(Container, app.extra["container"])  # type: ignore[unused-ignore]
    database = container.db()
    await database.create_tables()
    yield


def create_app() -> FastAPI:
    """Creates the FastAPI application."""

    container = Container()

    settings = container.app_settings()
    app = FastAPI(
        **settings.fastapi,
        lifespan=app_lifespan,
        container=container,
    )

    app.include_router(api_endpoints.router)

    errors.register_error_handlers(app)

    return app


app = create_app()
