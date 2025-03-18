from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from conduit.api.endpoints.articles.contract import (
    ArticleSlug,
    ArticleWithAuthorApiResponse,
)
from conduit.api.security.dependencies import CurrentUser
from conduit.application.articles.use_cases.favorite_article.use_case import (
    FavoriteArticleUseCase,
)
from conduit.containers import Container
from conduit.shared.api.openapi.not_found_error import not_found_error
from conduit.shared.api.openapi.tags import Tag
from conduit.shared.api.openapi.unauthorized_error import unauthorized_error

router = APIRouter()


@router.post(
    path="/articles/{slug}/favorite",
    responses={
        **unauthorized_error(),
        **not_found_error("Article"),
    },
    summary="Favorite an article",
    tags=[Tag.Articles],
)
@inject
async def favorite_article(
    slug: ArticleSlug,
    current_user: CurrentUser,
    favorite_article: FavoriteArticleUseCase = Depends(  # noqa: FAST002
        Provide[Container.favorite_article_use_case],
    ),
) -> ArticleWithAuthorApiResponse:
    article = await favorite_article(slug, current_user)
    if article is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found",
        )
    return ArticleWithAuthorApiResponse.from_article_with_author(article)
