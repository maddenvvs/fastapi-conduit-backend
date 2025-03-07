from typing import Any, final

from email_validator import EmailNotValidError, validate_email
from typing_extensions import Self

from conduit.domain.users.errors import Errors


@final
class EmailAddress(str):
    __slots__ = ()

    def __new__(cls, value: Any) -> Self:
        if type(value) is not str:
            raise Errors.invalid_email_type(value)

        try:
            validate_email(value, check_deliverability=False)
        except EmailNotValidError as exc:
            raise Errors.invalid_email_format(value) from exc

        return super().__new__(cls, value)
