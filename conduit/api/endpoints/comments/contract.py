from typing import Annotated, Optional, final

from fastapi import Path
from pydantic import BaseModel, Field
from typing_extensions import Self, TypeAlias

from conduit.api.json import DateTime
from conduit.domain.entities.comments import CommentWithAuthor

ArticleID: TypeAlias = Annotated[int, Path()]


@final
class NewCommentDetails(BaseModel):
    body: str = Field(
        description="The body of a new comment",
        min_length=1,
    )


@final
class CreateCommentApiRequest(BaseModel):
    comment: NewCommentDetails


@final
class CommentAuthor(BaseModel):
    username: str
    bio: str
    image: Optional[str]
    following: bool


@final
class CommentData(BaseModel):
    id: int
    created_at: DateTime
    updated_at: DateTime
    body: str
    author: CommentAuthor

    @classmethod
    def from_comment_with_author(cls, comment: CommentWithAuthor) -> Self:
        return cls(
            id=comment.id,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            body=comment.body,
            author=CommentAuthor(
                username="NO",
                bio="NO",
                image=None,
                following=False,
            ),
        )


@final
class CommentDetailsApiResponse(BaseModel):
    comment: CommentData

    @classmethod
    def from_comment_with_author(cls, comment: CommentWithAuthor) -> Self:
        return cls(
            comment=CommentData.from_comment_with_author(comment),
        )


@final
class ListCommentsApiResponse(BaseModel):
    comments: list[CommentData]

    @classmethod
    def from_comments(cls, comments: list[CommentWithAuthor]) -> Self:
        return cls(
            comments=[
                CommentData.from_comment_with_author(comment) for comment in comments
            ],
        )
