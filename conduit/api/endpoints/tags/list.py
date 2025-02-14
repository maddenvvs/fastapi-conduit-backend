from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from conduit.containers import Container
from conduit.domain.services.tags import TagsService


class ListTagsApiResponse(BaseModel):
    tags: list[str]


router = APIRouter()


@router.get(
    path="/tags",
    response_model=ListTagsApiResponse,
    tags=["Tags"],
)
@inject
async def get_all_tags(
    tags_service: TagsService = Depends(Provide[Container.tags_service]),
) -> ListTagsApiResponse:
    tags = await tags_service.get_all_tags()

    return ListTagsApiResponse(
        tags=[tag.name for tag in tags],
    )
