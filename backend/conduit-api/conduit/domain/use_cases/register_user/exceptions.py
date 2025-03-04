from typing import final

from conduit.domain.exceptions import DomainValidationError


@final
class EmailAlreadyTakenError(DomainValidationError):
    def __init__(self, *args: object) -> None:
        super().__init__(
            "email",
            "Email is taken",
            *args,
        )


@final
class UserNameAlreadyTakenError(DomainValidationError):
    def __init__(
        self,
        *args: object,
    ) -> None:
        super().__init__(
            "username",
            "Username is taken",
            *args,
        )
