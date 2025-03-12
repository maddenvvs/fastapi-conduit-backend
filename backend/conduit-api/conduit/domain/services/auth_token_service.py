import dataclasses
import datetime
import logging
from typing import Any, Optional

import jwt

from conduit.domain.entities.users import User, UserID

DEFAULT_LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class TokenPayload:
    user_id: UserID


class IncorrectJwtTokenError(Exception):
    pass


class AuthTokenService:
    """Service to handle JWT tokens."""

    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        token_expiration_minutes: int,
        logger: logging.Logger = DEFAULT_LOGGER,
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._token_expiration_minutes = token_expiration_minutes
        self._logger = logger

    def generate_jwt_token(
        self,
        user: User,
        current_time: Optional[datetime.datetime] = None,
    ) -> str:
        if current_time is None:
            current_time = datetime.datetime.now(datetime.timezone.utc)

        expire = current_time + datetime.timedelta(
            minutes=self._token_expiration_minutes,
        )
        payload: dict[str, Any] = {
            "user_id": user.id,
            "exp": expire,
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)  # type: ignore[unused-ignore]

    def parse_jwt_token(self, token: str) -> TokenPayload:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])  # type: ignore[unused-ignore]
        except jwt.InvalidTokenError as exc:
            self._logger.exception(
                "Invalid JWT token",
                extra={"token": token, "error": exc},
            )
            raise IncorrectJwtTokenError from exc

        return TokenPayload(
            user_id=payload["user_id"],
        )
