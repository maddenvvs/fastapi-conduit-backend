import contextlib

from fastapi import FastAPI

import conduit.api.endpoints as api_endpoints
from conduit.containers import Container
from conduit.persistence.database import Database


def app_lifespan(database: Database):

    @contextlib.asynccontextmanager
    async def lifespan(_: FastAPI):
        await database.create_tables()
        yield

    return lifespan


def create_app() -> FastAPI:
    """Creates the FastAPI application."""

    container = Container()

    settings = container.app_settings()
    lifespan = app_lifespan(container.db())
    app = FastAPI(
        **settings.fastapi,
        lifespan=lifespan,
        container=container,
    )

    app.include_router(api_endpoints.router)

    return app


app = create_app()
