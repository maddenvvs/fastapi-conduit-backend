from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from conduit.domain.exceptions import ValidationException


async def request_validation_error_handler(
    _: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "errors": exc.errors(),
        },
    )


async def domain_validation_error_handler(
    _: Request,
    exc: ValidationException,
) -> JSONResponse:
    error_details = {
        exc.field: [exc.reason],
    }
    return JSONResponse(
        status_code=422,
        content={
            "errors": error_details,
        },
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)  # type: ignore
    app.add_exception_handler(ValidationException, domain_validation_error_handler)  # type: ignore
