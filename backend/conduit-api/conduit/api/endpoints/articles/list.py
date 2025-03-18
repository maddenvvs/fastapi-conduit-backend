from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, status

from conduit.api.endpoints.articles.contract import (
    ListArticlesApiResponse,
    ListArticlesFilters,
)
from conduit.api.security.dependencies import OptionalCurrentUser
from conduit.application.articles.use_cases.list_articles.use_case import (
    ListArticlesUseCase,
)
from conduit.containers import Container
from conduit.shared.api.openapi.tags import Tag
from conduit.shared.api.openapi.unauthorized_error import unauthorized_error
from conduit.shared.api.openapi.validation_error import validation_error

router = APIRouter()


@router.get(
    path="/articles",
    responses={
        **unauthorized_error(),
        **validation_error(),
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
