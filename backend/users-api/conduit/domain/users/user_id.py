from typing import Any, final

from typing_extensions import Self

from conduit.domain.users.errors import Errors


@final
class UserId(int):
    def __new__(cls, value: Any) -> Self:
        if type(value) is not int:
            raise Errors.invalid_user_id(value)

        return super().__new__(cls, value)
