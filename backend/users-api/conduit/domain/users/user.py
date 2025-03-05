from dataclasses import dataclass
from typing import Optional

from typing_extensions import TypeAlias

UserId: TypeAlias = int


@dataclass(frozen=True)
class User:
    id: UserId
    username: str
    email: str
    bio: str
    image_url: Optional[str]
