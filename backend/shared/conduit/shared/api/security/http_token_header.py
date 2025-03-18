from enum import Enum, unique
from typing import Any, Optional, final

from fastapi import Request
from fastapi.security import APIKeyHeader

from conduit.shared.api.security.errors import Error


@final
@unique
class NoTokenStrategy(Enum):
    Silent = 0
    Raise = 1


@final
class HttpTokenHeader(APIKeyHeader):
    def __init__(self, error_strategy: NoTokenStrategy, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._error_strategy = error_strategy

    async def __call__(self, request: Request) -> Optional[str]:
        api_key = request.headers.get(self.model.name)

        if not api_key:
            if self._error_strategy is NoTokenStrategy.Raise:
                raise Error.missing_credentials()
            return ""

        try:
            token_prefix, token = api_key.split(" ")
        except ValueError as exc:
            raise Error.invalid_token_schema() from exc

        if token_prefix.lower() != "token":
            raise Error.invalid_token_schema()

        return token
