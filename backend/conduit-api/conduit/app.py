import contextlib
from collections.abc import AsyncIterator
from typing import cast

from fastapi import FastAPI

import conduit.api.endpoints.routes as api_endpoints
from conduit.api import errors
from conduit.containers import Container
from conduit.infrastructure.persistence.models import Base as ModelBase
from conduit.shared.api.openapi import tags


@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncIterator[None]:
    container = cast(Container, app.extra["container"])
    database = container.db()
    db_seeder = container.db_seeder()
    events_subsciber = container.events_subscriber()

    events_subsciber.start()

    if not await database.database_exists():
        await database.create_database(ModelBase)
        await db_seeder.seed_database()
    yield
    await database.dispose()


def create_app(container: Container) -> FastAPI:
    """Creates the FastAPI application."""

    settings = container.app_settings()
    app = FastAPI(
        title="Conduit Realworld REST API",
        summary="Implementation of Conduit Realworld API using FastAPI.",
        description="Inspirational link: [Realworld GitHub](https://github.com/gothinkster/realworld)",
        version="0.1.0",
        lifespan=app_lifespan,
        docs_url="/",
        openapi_tags=tags.tags_metadata(),
        redoc_url=None,  # Disable ReDoc documentaion
        container=container,
        **settings.fastapi,
    )

    app.include_router(api_endpoints.router)

    errors.register_error_handlers(app)

    return app


def build_app() -> FastAPI:
    container = Container()
    return create_app(container)


app = build_app()
