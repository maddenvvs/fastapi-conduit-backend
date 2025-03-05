from dataclasses import dataclass
from typing import Optional, final

from conduit.domain.users.user import UserId


@final
@dataclass(frozen=True)
class UpdatedUser:
    id: UserId
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    bio: Optional[str]
    image_url: Optional[str]
