from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from conduit.shared.api.errors.responses.validation_error import (
    ValidationErrorApiResponse,
)
from conduit.shared.application.errors import ApplicationError


async def request_validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    del request

    return ValidationErrorApiResponse.from_request_validation_error(
        exc,
    ).to_json_response()


async def application_error_handler(
    request: Request,
    exc: ApplicationError,
) -> JSONResponse:
    del request

    detail = exc.message or "Invalid request"
    return JSONResponse(
        content={"detail": detail},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


def register_error_handlers(app: FastAPI) -> None:
    app.exception_handler(RequestValidationError)(request_validation_error_handler)
    app.exception_handler(ApplicationError)(application_error_handler)
