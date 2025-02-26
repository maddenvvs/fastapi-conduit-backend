from typing import Any, Union, final

from fastapi import status
from pydantic import BaseModel, Field
from typing_extensions import TypeAlias

from conduit.api.errors import ValidationErrorApiResponse

OpenApiResponseDefinition: TypeAlias = dict[Union[int, str], dict[str, Any]]


def validation_error() -> OpenApiResponseDefinition:
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


def unauthorized_error_no_body() -> OpenApiResponseDefinition:
    return {
        status.HTTP_401_UNAUTHORIZED: {
            "model": HttpExceptionApiResponse,
            "description": "Unauthorized",
        },
    }


def unauthorized_error() -> OpenApiResponseDefinition:
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


def not_found_error(entity_name: str) -> OpenApiResponseDefinition:
    detail_message = f"{entity_name} not found"

    return {
        status.HTTP_404_NOT_FOUND: {
            "model": HttpExceptionApiResponse,
            "description": "Not Found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": detail_message,
                    }
                }
            },
        },
    }
