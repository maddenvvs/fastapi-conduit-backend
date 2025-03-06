from fastapi import status

from conduit.api.errors.responses.validation_error import ValidationErrorApiResponse
from conduit.api.openapi.response_definition import OpenApiResponseDefinition


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
                        },
                    },
                },
            },
        },
    }
