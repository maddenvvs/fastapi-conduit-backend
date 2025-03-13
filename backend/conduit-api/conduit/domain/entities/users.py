import uuid
from dataclasses import dataclass
from typing import Optional

from typing_extensions import TypeAlias

UserID: TypeAlias = int


@dataclass
class User:
    id: UserID
    user_id: uuid.UUID
    username: str
    bio: str
    image: Optional[str]
