from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from conduit.api.endpoints.articles.contract import (
    ArticleSlug,
    ArticleWithAuthorApiResponse,
)
from conduit.api.security.dependencies import OptionalCurrentUser
from conduit.application.articles.use_cases.get_article_by_slug.use_case import (
    GetArticleBySlugUseCase,
)
from conduit.containers import Container
from conduit.shared.api.openapi.not_found_error import not_found_error
from conduit.shared.api.openapi.tags import Tag
from conduit.shared.api.openapi.unauthorized_error import unauthorized_error

router = APIRouter()


@router.get(
    path="/articles/{slug}",
    responses={
        **unauthorized_error(),
        **not_found_error("Article"),
    },
    summary="Get article by slug",
    tags=[Tag.Articles],
)
@inject
async def get_article_by_slug(
    slug: ArticleSlug,
    optional_user: OptionalCurrentUser,
    get_article_by_slug: GetArticleBySlugUseCase = Depends(  # noqa: FAST002
        Provide[Container.get_article_by_slug_use_case],
    ),
) -> ArticleWithAuthorApiResponse:
    article = await get_article_by_slug(slug, optional_user)
    if article is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found",
        )

    return ArticleWithAuthorApiResponse.from_article_with_author(article)
