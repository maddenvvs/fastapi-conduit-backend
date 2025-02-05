from fastapi import APIRouter

from conduit.api.contract.responses.tags import GetAllTagsApiResponse
from conduit.api.dependencies import ITagsService

router = APIRouter(
    tags=["Tags"],
)


@router.get(
    path="/tags",
    response_model=GetAllTagsApiResponse,
)
async def get_all_tags(tags_service: ITagsService) -> GetAllTagsApiResponse:
    tags = await tags_service.get_all_tags()

    return GetAllTagsApiResponse(
        tags=[tag.name for tag in tags],
    )
