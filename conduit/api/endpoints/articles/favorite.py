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
from conduit.domain.use_cases.favorite_article.use_case import FavoriteArticleUseCase

router = APIRouter()


@router.post(
    path="/articles/{slug}/favorite",
    response_model=ArticleWithAuthorApiResponse,
    responses={
        **open_api.unauthorized_error(),
        **open_api.not_found_error("Article"),
    },
    summary="Favorite an article",
    tags=[Tag.Articles],
)
@inject
async def favorite_article(
    slug: ArticleSlug,
    current_user: CurrentUser,
    favorite_article: FavoriteArticleUseCase = Depends(
        Provide[Container.favorite_article_use_case]
    ),
) -> ArticleWithAuthorApiResponse:
    raise HTTPException(
        status_code=404,
        detail="Article is not found",
    )
