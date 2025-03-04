from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from conduit.api import open_api
from conduit.api.endpoints.articles.contract import ArticleSlug
from conduit.api.endpoints.comments.contract import ListCommentsApiResponse
from conduit.api.security.dependencies import OptionalCurrentUser
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.use_cases.list_comments.use_case import ListArticleCommentsUseCase

router = APIRouter()


@router.get(
    path="/articles/{slug}/comments",
    responses={
        **open_api.not_found_error("Article"),
        **open_api.validation_error(),
    },
    status_code=status.HTTP_200_OK,
    summary="List all comments of an article",
    tags=[Tag.Comments],
)
@inject
async def list_article_comments(
    slug: ArticleSlug,
    current_user: OptionalCurrentUser,
    list_comments: ListArticleCommentsUseCase = Depends(  # noqa: FAST002
        Provide[Container.list_article_comments_use_case],
    ),
) -> ListCommentsApiResponse:
    comments = await list_comments(slug, current_user)
    if comments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )

    return ListCommentsApiResponse.from_comments(comments)
