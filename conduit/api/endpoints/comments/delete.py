from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from conduit.api import open_api
from conduit.api.endpoints.articles.contract import ArticleSlug
from conduit.api.endpoints.comments.contract import ArticleID
from conduit.api.security.dependencies import CurrentUser
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.use_cases.delete_comment.use_case import DeleteArticleCommentUseCase

router = APIRouter()


@router.delete(
    path="/articles/{slug}/comments/{id}",
    responses={
        **open_api.unauthorized_error(),
        **open_api.not_found_error("Article"),
        **open_api.validation_error(),
    },
    status_code=status.HTTP_200_OK,
    summary="Delete a comment",
    tags=[Tag.Comments],
)
@inject
async def delete_article_comment(
    slug: ArticleSlug,
    id: ArticleID,
    current_user: CurrentUser,
    delete_comment: DeleteArticleCommentUseCase = Depends(
        Provide[Container.delete_article_comment_use_case]
    ),
) -> None:
    is_deleted = await delete_comment(
        slug=slug,
        comment_id=id,
        current_user=current_user,
    )
    if not is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
