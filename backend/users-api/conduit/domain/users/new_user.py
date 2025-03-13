from dataclasses import dataclass
from typing import final

from conduit.domain.users.user_id import UserId


@final
@dataclass(frozen=True)
class NewUser:
    user_id: UserId
    username: str
    email: str
    password: str
