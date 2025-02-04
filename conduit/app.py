from fastapi import FastAPI

import conduit.api.routes as api_routes


def create_app() -> FastAPI:
    """Creates the FastAPI application."""

    application = FastAPI()

    application.include_router(api_routes.router)

    return application


app = create_app()
