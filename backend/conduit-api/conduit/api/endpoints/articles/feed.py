from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, status

from conduit.api.endpoints.articles.contract import (
    ListArticlesApiResponse,
    PagingParameters,
)
from conduit.api.security.dependencies import CurrentUser
from conduit.containers import Container
from conduit.domain.use_cases.feed_articles.use_case import FeedArticlesUseCase
from conduit.shared.api.openapi.tags import Tag
from conduit.shared.api.openapi.unauthorized_error import unauthorized_error
from conduit.shared.api.openapi.validation_error import validation_error

router = APIRouter()


@router.get(
    path="/articles/feed",
    responses={
        **unauthorized_error(),
        **validation_error(),
    },
    status_code=status.HTTP_200_OK,
    summary="Personal articles feed",
    tags=[Tag.Articles],
)
@inject
async def feed_articles(
    current_user: CurrentUser,
    paging: Annotated[PagingParameters, Query()],
    use_case: FeedArticlesUseCase = Depends(Provide[Container.feed_articles_use_case]),  # noqa: FAST002
) -> ListArticlesApiResponse:
    articles_info = await use_case(paging.to_domain(current_user))
    return ListArticlesApiResponse.from_feed_info(articles_info)
