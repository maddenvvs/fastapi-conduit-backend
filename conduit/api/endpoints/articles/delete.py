from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from conduit.api import open_api
from conduit.api.endpoints.articles.contract import ArticleSlug
from conduit.api.security.dependencies import CurrentUser
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.use_cases.delete_article_by_slug.use_case import (
    DeleteArticleBySlugUseCase,
)

router = APIRouter()


@router.delete(
    path="/articles/{slug}",
    responses={
        **open_api.unauthorized_error(),
        **open_api.not_found_error("Article"),
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
