from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, status

from conduit.api import open_api
from conduit.api.endpoints.articles.contract import ListArticlesApiResponse
from conduit.api.security.dependencies import CurrentUser
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.use_cases.feed_articles.use_case import (
    FeedArticlesRequest,
    FeedArticlesUseCase,
)

router = APIRouter()


@router.get(
    path="/articles/feed",
    response_model=ListArticlesApiResponse,
    responses={
        **open_api.unauthorized_error(),
        **open_api.validation_error(),
    },
    status_code=status.HTTP_200_OK,
    summary="Personal articles feed",
    tags=[Tag.Articles],
)
@inject
async def feed_articles(
    current_user: CurrentUser,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    use_case: FeedArticlesUseCase = Depends(Provide[Container.feed_articles_use_case]),
) -> ListArticlesApiResponse:
    articles_info = await use_case(
        FeedArticlesRequest(
            limit=limit,
            offset=offset,
            user=current_user,
        )
    )
    return ListArticlesApiResponse.from_feed_info(articles_info)
