from typing import Any, Optional, final

import starlette.status as http_status
from fastapi import Request
from fastapi.security import APIKeyHeader
from starlette.exceptions import HTTPException


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

            raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail="Missing authorization credentials.",
            )

        try:
            token_prefix, token = api_key.split(" ")
        except ValueError:
            raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token schema.",
            )

        if token_prefix.lower() != "token":
            raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token schema.",
            )

        return token
