from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException

from conduit.api import open_api
from conduit.api.endpoints.articles.contract import (
    ArticleSlug,
    ArticleWithAuthorApiResponse,
    UpdateArticleApiRequest,
)
from conduit.api.security.dependencies import CurrentUser
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.use_cases.update_article.use_case import UpdateArticleUseCase

router = APIRouter()


@router.put(
    path="/articles/{slug}",
    responses={
        **open_api.unauthorized_error(),
        **open_api.not_found_error("Article"),
        **open_api.validation_error(),
    },
    summary="Update an article",
    tags=[Tag.Articles],
)
@inject
async def update_article(
    slug: ArticleSlug,
    request: Annotated[UpdateArticleApiRequest, Body()],
    current_user: CurrentUser,
    update_article: UpdateArticleUseCase = Depends(  # noqa: FAST002
        Provide[Container.update_article_use_case],
    ),
) -> ArticleWithAuthorApiResponse:
    article = await update_article(slug, request.to_domain(), current_user)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return ArticleWithAuthorApiResponse.from_article_with_author(article)
