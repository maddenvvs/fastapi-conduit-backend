from fastapi import status

from conduit.shared.api.errors.responses.http_exception import HttpExceptionApiResponse
from conduit.shared.api.openapi.response_definition import OpenApiResponseDefinition


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
                    },
                },
            },
        },
    }
