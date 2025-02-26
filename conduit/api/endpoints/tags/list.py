from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing_extensions import Self

from conduit.api import tags
from conduit.containers import Container
from conduit.domain.entities.tags import Tag
from conduit.domain.use_cases.list_tags.use_case import ListTagsUseCase


class ListTagsApiResponse(BaseModel):
    tags: list[str]

    @classmethod
    def from_tags(cls, tags: list[Tag]) -> Self:
        return cls(tags=[tag.name for tag in tags])


router = APIRouter()


@router.get(
    path="/tags",
    response_model=ListTagsApiResponse,
    summary="List all tags",
    tags=[tags.Tag.Tags],
)
@inject
async def get_all_tags(
    list_tags: ListTagsUseCase = Depends(Provide[Container.list_tags_use_case]),
) -> ListTagsApiResponse:
    tags = await list_tags()
    return ListTagsApiResponse.from_tags(tags)
