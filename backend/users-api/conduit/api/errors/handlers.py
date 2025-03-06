from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from conduit.api.errors.responses.validation_error import ValidationErrorApiResponse


async def request_validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    del request

    return ValidationErrorApiResponse.from_request_validation_error(
        exc,
    ).to_json_response()


def register_error_handlers(app: FastAPI) -> None:
    app.exception_handler(RequestValidationError)(request_validation_error_handler)
