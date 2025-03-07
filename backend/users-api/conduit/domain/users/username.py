from typing import Any, Final, final

from typing_extensions import Self

from conduit.domain.users.errors import Errors

MAX_USERNAME_LENGTH: Final = 20


@final
class Username(str):
    __slots__ = ()

    def __new__(cls, value: Any) -> Self:
        if type(value) is not str:
            raise Errors.invalid_username(value)

        is_valid_length = 0 < len(value) < MAX_USERNAME_LENGTH
        if not is_valid_length:
            raise Errors.invalid_username_length(
                min_length=1,
                max_length=MAX_USERNAME_LENGTH,
            )

        return super().__new__(cls, value)
