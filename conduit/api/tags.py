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


OPEN_API_TAGS_METADATA: Final = [
    dict(
        name=Tag.Articles,
        description="Here you can *CRUD* articles. Supporting two types of feeds (global and personal).",
    ),
    dict(
        name=Tag.Comments,
        description="Here you can *CRD* comments.",
    ),
    dict(
        name=Tag.Users,
        description="Operations with users. The **login** logic is also here.",
    ),
    dict(
        name=Tag.Profiles,
        description="Operations with profiles.",
    ),
    dict(
        name=Tag.Tags,
        description="Lists all available tags.",
    ),
    dict(
        name=Tag.Health,
        description="Infrastructural endpoints required for maintenance.",
    ),
]


def open_api_tags_metadata() -> list[dict[str, Any]]:
    return OPEN_API_TAGS_METADATA
