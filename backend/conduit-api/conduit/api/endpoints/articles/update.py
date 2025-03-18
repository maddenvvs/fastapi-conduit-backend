from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException

from conduit.api.endpoints.articles.contract import (
    ArticleSlug,
    ArticleWithAuthorApiResponse,
    UpdateArticleApiRequest,
)
from conduit.api.security.dependencies import CurrentUser
from conduit.application.articles.use_cases.update_article.use_case import (
    UpdateArticleUseCase,
)
from conduit.containers import Container
from conduit.shared.api.openapi.not_found_error import not_found_error
from conduit.shared.api.openapi.tags import Tag
from conduit.shared.api.openapi.unauthorized_error import unauthorized_error
from conduit.shared.api.openapi.validation_error import validation_error

router = APIRouter()


@router.put(
    path="/articles/{slug}",
    responses={
        **unauthorized_error(),
        **not_found_error("Article"),
        **validation_error(),
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
