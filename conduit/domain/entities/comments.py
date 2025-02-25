import datetime
from dataclasses import dataclass, field
from typing import Optional, final

from typing_extensions import TypeAlias

from conduit.domain.entities.articles import ArticleID
from conduit.domain.entities.users import UserID

CommentID: TypeAlias = int


@final
@dataclass
class CommentAuthor:
    username: str
    bio: str
    image: Optional[str] = field(default=None)
    following: bool = field(default=False)


@final
@dataclass
class CommentWithAuthor:
    id: CommentID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    body: str
    author: CommentAuthor


@final
@dataclass
class NewComment:
    article_id: ArticleID
    author_id: UserID
    body: str


@final
@dataclass
class Comment:
    id: CommentID
    article_id: ArticleID
    author_id: UserID
    body: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
