from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException, status

from conduit.api import open_api
from conduit.api.endpoints.articles.contract import ArticleSlug
from conduit.api.endpoints.comments.contract import (
    CommentDetailsApiResponse,
    CreateCommentApiRequest,
)
from conduit.api.security.dependencies import CurrentUser
from conduit.api.tags import Tag
from conduit.containers import Container
from conduit.domain.use_cases.add_comment.use_case import AddCommentToArticleUseCase

router = APIRouter()


@router.post(
    path="/articles/{slug}/comments",
    response_model=CommentDetailsApiResponse,
    responses={
        **open_api.unauthorized_error(),
        **open_api.not_found_error("Article"),
        **open_api.validation_error(),
    },
    status_code=status.HTTP_201_CREATED,
    summary="Add comment to an article",
    tags=[Tag.Comments],
)
@inject
async def add_comment_to_article(
    slug: ArticleSlug,
    comment_request: Annotated[CreateCommentApiRequest, Body()],
    current_user: CurrentUser,
    add_comment: AddCommentToArticleUseCase = Depends(
        Provide[Container.add_comment_to_article_use_case]
    ),
) -> CommentDetailsApiResponse:
    created_comment = await add_comment(
        slug, comment_request.comment.body, current_user
    )
    if created_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )

    return CommentDetailsApiResponse.from_domain(created_comment)
