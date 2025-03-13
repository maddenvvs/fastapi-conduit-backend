from typing import Optional, final

from pydantic import BaseModel, HttpUrl


@final
class UserCreatedMessage(BaseModel):
    user_id: str
    username: str
    bio: str
    image_url: Optional[HttpUrl]
