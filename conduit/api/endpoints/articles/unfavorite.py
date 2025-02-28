from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from conduit.api import open_api
from conduit.api.endpoints.articles.contract import (
    ArticleSlug,
    ArticleWithAuthorApiResponse,
)
from conduit.api.security.dependencies import CurrentUser
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.use_cases.unfavorite_article.use_case import (
    UnfavoriteArticleUseCase,
)

router = APIRouter()


@router.delete(
    path="/articles/{slug}/favorite",
    response_model=ArticleWithAuthorApiResponse,
    responses={
        **open_api.unauthorized_error(),
        **open_api.not_found_error("Article"),
    },
    summary="Unfavorite an article",
    tags=[Tag.Articles],
)
@inject
async def unfavorite_article(
    slug: ArticleSlug,
    current_user: CurrentUser,
    unfavorite_article: UnfavoriteArticleUseCase = Depends(
        Provide[Container.unfavorite_article_use_case]
    ),
) -> ArticleWithAuthorApiResponse:
    article = await unfavorite_article(slug, current_user)
    if article is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found",
        )
    return ArticleWithAuthorApiResponse.from_article_with_author(article)
