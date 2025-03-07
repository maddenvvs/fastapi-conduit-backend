from dataclasses import dataclass
from typing import Optional, final

from conduit.domain.users.user_id import UserId
from conduit.domain.users.username import Username


@final
@dataclass(frozen=True)
class User:
    id: UserId
    username: Username
    email: str
    bio: str
    image_url: Optional[str]
