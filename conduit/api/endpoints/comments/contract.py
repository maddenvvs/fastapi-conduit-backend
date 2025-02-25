from typing import Optional, final

from pydantic import BaseModel, Field
from typing_extensions import Self

from conduit.api.json import DateTime
from conduit.domain.entities.comments import CommentWithAuthor


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
class CommentDetails(BaseModel):
    id: int
    created_at: DateTime
    updated_at: DateTime
    body: str
    author: CommentAuthor

    @classmethod
    def from_domain(cls, comment: CommentWithAuthor) -> Self:
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
    comment: CommentDetails

    @classmethod
    def from_domain(cls, comment: CommentWithAuthor) -> Self:
        return cls(
            comment=CommentDetails.from_domain(comment),
        )


@final
class ListCommentsApiResponse(BaseModel):
    comments: list[CommentDetails]

    @classmethod
    def from_domain(cls, comments: list[CommentWithAuthor]) -> Self:
        return cls(
            comments=[CommentDetails.from_domain(comment) for comment in comments],
        )
