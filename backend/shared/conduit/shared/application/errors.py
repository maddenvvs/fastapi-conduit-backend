from typing import final


class ApplicationError(Exception):
    """Base class for application exceptions."""

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.message = message


@final
class InvalidCredentialsError(ApplicationError):
    def __init__(self, *args: object) -> None:
        super().__init__("Invalid credentials", *args)


@final
class Errors:
    @staticmethod
    def invalid_credentials() -> InvalidCredentialsError:
        return InvalidCredentialsError()
