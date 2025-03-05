from typing import Any, Optional, final

from fastapi import Request
from fastapi.security import APIKeyHeader

from conduit.api.security.errors import Error


@final
class HttpTokenHeader(APIKeyHeader):
    def __init__(self, raise_error: bool, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._raise_error = raise_error

    async def __call__(self, request: Request) -> Optional[str]:
        api_key = request.headers.get(self.model.name)
        if not api_key:
            if not self._raise_error:
                return ""

            raise Error.missing_credentials()

        try:
            token_prefix, token = api_key.split(" ")
        except ValueError as exc:
            raise Error.invalid_token_schema() from exc

        if token_prefix.lower() != "token":
            raise Error.invalid_token_schema()

        return token
