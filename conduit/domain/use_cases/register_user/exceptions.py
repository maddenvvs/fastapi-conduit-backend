from typing import final

from conduit.domain.exceptions import DomainValidationException


@final
class EmailAlreadyTakenException(DomainValidationException):
    def __init__(self, email: str, *args: object) -> None:
        super().__init__(
            "email",
            f"Email '{email}' is already taken",
            *args,
        )


@final
class UserNameAlreadyTakenException(DomainValidationException):
    def __init__(
        self,
        username: str,
        *args: object,
    ) -> None:
        super().__init__(
            "username",
            f"Username '{username}' is already taken",
            *args,
        )
