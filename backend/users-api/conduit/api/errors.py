from collections.abc import Sequence
from typing import Any, Optional, final

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing_extensions import Self

# from conduit.domain.exceptions import DomainError, DomainValidationError
# from conduit.domain.use_cases.login_user.exceptions import InvalidCredentialsError


@final
class HttpExceptionApiResponse(BaseModel):
    detail: str = Field(
        description="Detailed error message.",
        examples=["Missing authorization credentials"],
    )


@final
class ValidationErrorApiResponse(BaseModel):
    errors: dict[str, list[str]] = Field(
        description="Field validation error details for each field.",
    )

    def to_json_response(self) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=self.model_dump(),
        )

    #     @classmethod
    #     def from_domain_validation_exception(cls, exc: DomainValidationError) -> Self:
    #         return cls(errors={exc.field: [exc.reason]})

    @staticmethod
    def _convert_to_errors_dict(errors: Sequence[Any]) -> dict[str, list[str]]:
        errors_dict: dict[str, list[str]] = {}

        error: dict[str, Any]
        for error in errors:
            # Error structure to parse (https://docs.pydantic.dev/latest/errors/errors/)
            """
            {
                'type': 'value_error',
                'loc': ('body', 'user', 'email'),
                'msg': 'value is not a valid email address: An email address must have an @-sign.',
                'input': 'userxample.com',
                'ctx': {'reason': 'An email address must have an @-sign.'}
            }
            """

            field_path: Optional[tuple[str, ...]] = error.get("loc", None)
            if field_path is None or len(field_path) == 0:
                field_name = "_request"
            else:
                field_name = str(field_path[-1])

            message = error.get("msg", "")
            context = error.get("ctx", {})
            reason = context.get("reason", "")

            error_message = reason or message or "Invalid request"

            if errors_dict.get(field_name) is None:
                errors_dict[field_name] = []

            errors_dict[field_name].append(error_message)

        return errors_dict

    @classmethod
    def from_request_validation_error(cls, exc: RequestValidationError) -> Self:
        errors = cls._convert_to_errors_dict(exc.errors())
        return cls(errors=errors)


async def request_validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return ValidationErrorApiResponse.from_request_validation_error(
        exc,
    ).to_json_response()

    # async def domain_validation_error_handler(
    #     _request: Request,
    #     exc: DomainValidationError,
    # ) -> JSONResponse:
    #     return ValidationErrorApiResponse.from_domain_validation_exception(
    #         exc,
    #     ).to_json_response()

    # async def domain_error_handler(
    #     _request: Request,
    #     exc: DomainError,
    # ) -> JSONResponse:
    #     detail = exc.args[0] if exc.args else "Invalid request"
    #     return JSONResponse(
    #         content={"detail": detail},
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #     )

    # async def invalid_credentials_error_handler(
    #     _request: Request,
    #     _exc: InvalidCredentialsError,
    # ) -> JSONResponse:
    #     return JSONResponse(content=None, status_code=status.HTTP_401_UNAUTHORIZED)


def register_error_handlers(app: FastAPI) -> None:
    app.exception_handler(RequestValidationError)(request_validation_error_handler)


#     app.exception_handler(DomainValidationError)(domain_validation_error_handler)
#     app.exception_handler(InvalidCredentialsError)(invalid_credentials_error_handler)
#     app.exception_handler(DomainError)(domain_error_handler)
