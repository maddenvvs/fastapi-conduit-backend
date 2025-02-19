class DomainException(Exception):
    """Base domain exception."""


class DomainValidationException(DomainException):
    """Base validation exception."""

    def __init__(
        self,
        field: str,
        reason: str,
        *args: object,
    ) -> None:
        super().__init__(*args)

        self.field = field
        self.reason = reason
