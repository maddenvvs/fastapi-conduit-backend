from typing import Any, Union, final

from fastapi import status
from pydantic import BaseModel, Field

from conduit.api.errors import ValidationErrorApiResponse


def validation_error() -> dict[Union[int, str], dict[str, Any]]:
    return {
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ValidationErrorApiResponse,
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "errors": {
                            "field_1": [
                                "value is too long",
                            ],
                            "field_2": [
                                "value cannot be empty",
                            ],
                        }
                    }
                }
            },
        },
    }


@final
class HttpExceptionApiResponse(BaseModel):
    detail: str = Field(
        description="Detailed error message.",
        examples=["Missing authorization credentials"],
    )


def unauthorized_error() -> dict[Union[int, str], dict[str, Any]]:
    return {
        status.HTTP_401_UNAUTHORIZED: {
            "model": HttpExceptionApiResponse,
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Missing authorization credentials",
                    }
                }
            },
        },
    }
