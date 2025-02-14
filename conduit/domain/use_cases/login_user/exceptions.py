from typing import final

from conduit.domain.exceptions import ValidationException


@final
class InvalidCredentialsException(ValidationException):
    def __init__(self, field: str, reason: str, *args: object) -> None:
        super().__init__(field, reason, *args)
