from pydantic import BaseModel
from typing_extensions import Self

from conduit.domain.entities.tags import Tag


class ListTagsApiResponse(BaseModel):
    tags: list[str]

    @classmethod
    def from_tags(cls, tags: list[Tag]) -> Self:
        return cls(tags=[tag.name for tag in tags])
