from typing import Optional, final

from pydantic import BaseModel, HttpUrl
from typing_extensions import Self

from conduit.domain.users.events.user_created import UserCreatedEvent


@final
class UserCreatedMessage(BaseModel):
    user_id: str
    username: str
    email: str
    bio: str
    image_url: Optional[HttpUrl]

    @classmethod
    def from_event(cls, event: UserCreatedEvent) -> Self:
        return cls(
            user_id=str(event.user_id),
            username=event.username,
            email=event.email,
            bio=event.bio,
            image_url=event.image_url,
        )
