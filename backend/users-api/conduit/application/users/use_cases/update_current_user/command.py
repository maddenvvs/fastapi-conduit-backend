from dataclasses import dataclass
from typing import Optional, final

from conduit.domain.users.user import User


@final
@dataclass(frozen=True)
class UpdateCurrentUserCommand:
    current_user: User
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    bio: Optional[str]
    image_url: Optional[str]
