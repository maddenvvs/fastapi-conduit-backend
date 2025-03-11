from typing import Optional, final

from pydantic import BaseModel, HttpUrl
from typing_extensions import Self

from conduit.domain.users.events.user_created import UserCreatedEvent


@final
class UserCreatedMessage(BaseModel):
    user_id: int
    username: str
    bio: str
    image_url: Optional[HttpUrl]

    @classmethod
    def from_event(cls, event: UserCreatedEvent) -> Self:
        return cls(
            user_id=event.user_id,
            username=event.username,
            bio=event.bio,
            image_url=event.image_url,
        )
