from enum import Enum, unique
from typing import Any, Final, final


@final
@unique
class Tag(Enum):
    Articles = "Articles"
    Comments = "Comments"
    Health = "Health"
    Profiles = "Profiles"
    Tags = "Tags"
    Users = "Users"


OPEN_API_TAGS_METADATA: Final[list[dict[str, Any]]] = [
    {
        "name": Tag.Articles,
        "description": "Here you can *CRUD* articles. Supporting two types of feeds (global and personal).",
    },
    {
        "name": Tag.Comments,
        "description": "Here you can *CRD* comments.",
    },
    {
        "name": Tag.Profiles,
        "description": "Operations with profiles.",
    },
    {
        "name": Tag.Tags,
        "description": "Lists all available tags.",
    },
    {
        "name": Tag.Health,
        "description": "Infrastructural endpoints required for maintenance.",
    },
    {
        "name": Tag.Users,
        "description": "Operations with users. The **login** logic is also here.",
    },
]


def tags_metadata() -> list[dict[str, Any]]:
    return OPEN_API_TAGS_METADATA
