from dataclasses import dataclass
from typing import Optional, final

from conduit.domain.users.image_url import ImageUrl
from conduit.domain.users.user_id import UserId
from conduit.domain.users.username import Username


@final
@dataclass(frozen=True)
class UserUpdatedEvent:
    user_id: UserId
    username: Username
    bio: str
    image_url: Optional[ImageUrl]
