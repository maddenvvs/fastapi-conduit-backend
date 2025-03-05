from typing import final

import starlette.status as http_status
from starlette.exceptions import HTTPException


@final
class Error:
    @staticmethod
    def invalid_token_schema() -> HTTPException:
        return HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token schema",
        )

    @staticmethod
    def missing_credentials() -> HTTPException:
        return HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization credentials",
        )
