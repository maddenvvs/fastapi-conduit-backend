from typing import Any, Union

from fastapi import status

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
