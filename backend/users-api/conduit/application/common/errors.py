from typing import final

from conduit.shared.application.errors import ApplicationError


@final
class EmailTakenError(ApplicationError):
    def __init__(self, *args: object) -> None:
        super().__init__("Email is already in use", *args)


@final
class UsernameTakenError(ApplicationError):
    def __init__(self, *args: object) -> None:
        super().__init__("Username is already in use", *args)


@final
class Errors:
    @staticmethod
    def email_is_taken() -> EmailTakenError:
        return EmailTakenError()

    @staticmethod
    def username_is_taken() -> UsernameTakenError:
        return UsernameTakenError()
