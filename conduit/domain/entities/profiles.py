from dataclasses import dataclass, field
from typing import Optional, final

from typing_extensions import TypeAlias

ProfileID: TypeAlias = int


@final
@dataclass(frozen=True)
class Profile:
    id: ProfileID
    username: str
    bio: str
    image: Optional[str] = field(default=None)
    following: bool = field(default=False)
