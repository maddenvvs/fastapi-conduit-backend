from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, status

from conduit.api import open_api
from conduit.api.endpoints.articles.contract import (
    ListArticlesApiResponse,
    ListArticlesFilters,
)
from conduit.api.security.dependencies import OptionalCurrentUser
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.use_cases.list_articles.use_case import ListArticlesUseCase

router = APIRouter()


@router.get(
    path="/articles",
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
    filters: Annotated[ListArticlesFilters, Query()],
    use_case: ListArticlesUseCase = Depends(Provide[Container.list_articles_use_case]),  # noqa: FAST002
) -> ListArticlesApiResponse:
    articles_info = await use_case(filters.to_domain(optional_user))
    return ListArticlesApiResponse.from_articles_info(articles_info)
