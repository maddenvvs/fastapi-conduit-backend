from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Path, status

from conduit.api.endpoints.articles.contract import ArticleSlug
from conduit.api.security.dependencies import CurrentUser
from conduit.application.comments.use_cases.delete_comment.use_case import (
    DeleteArticleCommentUseCase,
)
from conduit.containers import Container
from conduit.shared.api.openapi.not_found_error import not_found_error
from conduit.shared.api.openapi.tags import Tag
from conduit.shared.api.openapi.unauthorized_error import unauthorized_error
from conduit.shared.api.openapi.validation_error import validation_error

router = APIRouter()


@router.delete(
    path="/articles/{slug}/comments/{comment_id}",
    responses={
        **unauthorized_error(),
        **not_found_error("Article"),
        **validation_error(),
    },
    status_code=status.HTTP_200_OK,
    summary="Delete a comment",
    tags=[Tag.Comments],
)
@inject
async def delete_article_comment(
    slug: ArticleSlug,
    comment_id: Annotated[int, Path()],
    current_user: CurrentUser,
    delete_comment: DeleteArticleCommentUseCase = Depends(  # noqa: FAST002
        Provide[Container.delete_article_comment_use_case],
    ),
) -> None:
    is_deleted = await delete_comment(slug, comment_id, current_user)
    if not is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
