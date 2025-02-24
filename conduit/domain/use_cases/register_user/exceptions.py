from typing import final

from conduit.domain.exceptions import DomainValidationException


@final
class EmailAlreadyTakenException(DomainValidationException):
    def __init__(self, *args: object) -> None:
        super().__init__(
            "email",
            f"Email is taken",
            *args,
        )


@final
class UserNameAlreadyTakenException(DomainValidationException):
    def __init__(
        self,
        *args: object,
    ) -> None:
        super().__init__(
            "username",
            f"Username is taken",
            *args,
        )
