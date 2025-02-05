from fastapi import FastAPI

import conduit.api.endpoints as api_endpoints


def create_app() -> FastAPI:
    """Creates the FastAPI application."""

    application = FastAPI()

    application.include_router(api_endpoints.router)

    return application


app = create_app()
