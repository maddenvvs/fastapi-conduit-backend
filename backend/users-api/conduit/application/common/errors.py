from typing import final


class ApplicationError(Exception):
    """Base class for application exceptions."""

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.message = message


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
