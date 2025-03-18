from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from conduit.api.endpoints.articles.contract import ArticleSlug
from conduit.api.security.dependencies import CurrentUser
from conduit.containers import Container
from conduit.domain.use_cases.delete_article_by_slug.use_case import (
    DeleteArticleBySlugUseCase,
)
from conduit.shared.api.openapi.not_found_error import not_found_error
from conduit.shared.api.openapi.tags import Tag
from conduit.shared.api.openapi.unauthorized_error import unauthorized_error

router = APIRouter()


@router.delete(
    path="/articles/{slug}",
    responses={
        **unauthorized_error(),
        **not_found_error("Article"),
    },
    summary="Delete article by its slug",
    tags=[Tag.Articles],
)
@inject
async def delete_article(
    slug: ArticleSlug,
    current_user: CurrentUser,
    delete_article: DeleteArticleBySlugUseCase = Depends(  # noqa: FAST002
        Provide[Container.delete_article_by_slug_use_case],
    ),
) -> None:
    await delete_article(slug, current_user)
