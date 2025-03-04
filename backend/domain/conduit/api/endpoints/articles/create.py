from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, status

from conduit.api import open_api
from conduit.api.endpoints.articles.contract import (
    ArticleWithAuthorApiResponse,
    CreateArticleApiRequest,
)
from conduit.api.security.dependencies import CurrentUser
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.use_cases.create_article.use_case import CreateArticleUseCase

router = APIRouter()


@router.post(
    path="/articles",
    responses={
        **open_api.unauthorized_error(),
        **open_api.validation_error(),
    },
    status_code=status.HTTP_201_CREATED,
    summary="Create a new article",
    tags=[Tag.Articles],
)
@inject
async def create_article(
    new_article: Annotated[CreateArticleApiRequest, Body()],
    current_user: CurrentUser,
    create_article: CreateArticleUseCase = Depends(  # noqa: FAST002
        Provide[Container.create_article_use_case],
    ),
) -> ArticleWithAuthorApiResponse:
    created_article = await create_article(new_article.to_domain(), current_user)
    return ArticleWithAuthorApiResponse.from_article_with_author(created_article)
