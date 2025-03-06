from fastapi import status

from conduit.api.errors.responses.http_exception import HttpExceptionApiResponse
from conduit.api.openapi.response_definition import OpenApiResponseDefinition


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
                    },
                },
            },
        },
    }
