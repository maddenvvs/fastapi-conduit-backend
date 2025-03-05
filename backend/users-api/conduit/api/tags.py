from enum import Enum, unique
from typing import Any, Final, final


@final
@unique
class Tag(Enum):
    Users = "Users"


OPEN_API_TAGS_METADATA: Final[list[dict[str, Any]]] = [
    {
        "name": Tag.Users,
        "description": "Operations with users. The **login** logic is also here.",
    },
]


def open_api_tags_metadata() -> list[dict[str, Any]]:
    return OPEN_API_TAGS_METADATA
