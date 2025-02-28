from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from conduit.api import tags
from conduit.api.endpoints.tags.contract import ListTagsApiResponse
from conduit.containers import Container
from conduit.domain.use_cases.list_tags.use_case import ListTagsUseCase

router = APIRouter()


@router.get(
    path="/tags",
    summary="List all tags",
    tags=[tags.Tag.Tags],
)
@inject
async def get_all_tags(
    list_tags: ListTagsUseCase = Depends(Provide[Container.list_tags_use_case]),  # noqa: FAST002
) -> ListTagsApiResponse:
    tags = await list_tags()
    return ListTagsApiResponse.from_tags(tags)
