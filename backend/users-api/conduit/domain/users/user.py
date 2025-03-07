from dataclasses import dataclass
from typing import Optional, final

from conduit.domain.users.user_id import UserId


@final
@dataclass(frozen=True)
class User:
    id: UserId
    username: str
    email: str
    bio: str
    image_url: Optional[str]
