class DomainError(Exception):
    """Base domain exception."""


class DomainValidationError(DomainError):
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
