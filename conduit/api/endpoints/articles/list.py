from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, status

from conduit.api import open_api
from conduit.api.endpoints.articles.contract import ListArticlesApiResponse
from conduit.api.security.dependencies import OptionalCurrentUser
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.use_cases.list_articles.use_case import (
    ListArticlesRequest,
    ListArticlesUseCase,
)

router = APIRouter()


@router.get(
    path="/articles",
    response_model=ListArticlesApiResponse,
    responses={
        **open_api.unauthorized_error(),
        **open_api.validation_error(),
    },
    status_code=status.HTTP_200_OK,
    summary="List all articles",
    tags=[Tag.Articles],
)
@inject
async def list_articles(
    optional_user: OptionalCurrentUser,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    use_case: ListArticlesUseCase = Depends(Provide[Container.list_articles_use_case]),
) -> ListArticlesApiResponse:
    articles_info = await use_case(
        ListArticlesRequest(limit=limit, offset=offset, user=optional_user)
    )
    return ListArticlesApiResponse.from_articles_info(articles_info)
