from typing import Any, Final

from conduit.api.tags import Tag

OPEN_API_TAGS_METADATA: Final[list[dict[str, Any]]] = [
    {
        "name": Tag.Users,
        "description": "Operations with users. The **login** logic is also here.",
    },
]


def tags_metadata() -> list[dict[str, Any]]:
    return OPEN_API_TAGS_METADATA
