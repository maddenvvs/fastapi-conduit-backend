from dataclasses import dataclass
from typing import Optional, final

from typing_extensions import override

from conduit.domain.users.email_address import EmailAddress
from conduit.domain.users.image_url import ImageUrl
from conduit.domain.users.user_id import UserId
from conduit.domain.users.username import Username


@final
@dataclass(frozen=True, eq=False)
class User:
    id: UserId
    username: Username
    email: EmailAddress
    bio: str
    image_url: Optional[ImageUrl]

    @override
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, User):
            return False
        return self.id == value.id

    @override
    def __hash__(self) -> int:
        return hash(self.id)
