from typing import Optional, final

from pydantic import BaseModel, HttpUrl
from typing_extensions import Self

from conduit.domain.users.events.user_updated import UserUpdatedEvent


@final
class UserUpdatedMessage(BaseModel):
    user_id: str
    username: str
    bio: str
    image_url: Optional[HttpUrl]

    @classmethod
    def from_event(cls, event: UserUpdatedEvent) -> Self:
        return cls(
            user_id=str(event.user_id),
            username=event.username,
            bio=event.bio,
            image_url=event.image_url,
        )
