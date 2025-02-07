from fastapi import APIRouter
from pydantic import BaseModel

from conduit.api.dependencies import ITagsService


class ListTagsApiResponse(BaseModel):
    tags: list[str]


router = APIRouter()


@router.get(
    path="/tags",
    response_model=ListTagsApiResponse,
    tags=["Tags"],
)
async def get_all_tags(tags_service: ITagsService) -> ListTagsApiResponse:
    tags = await tags_service.get_all_tags()

    return ListTagsApiResponse(
        tags=[tag.name for tag in tags],
    )
