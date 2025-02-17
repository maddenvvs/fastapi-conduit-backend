from dataclasses import dataclass, field
from typing import Optional, final


@final
@dataclass(frozen=True)
class Profile:
    id: int
    username: str
    bio: str
    image: Optional[str] = field(default=None)
    following: bool = field(default=False)
