from typing import final

from conduit.domain.exceptions import DomainError


@final
class InvalidCredentialsError(DomainError):
    pass
