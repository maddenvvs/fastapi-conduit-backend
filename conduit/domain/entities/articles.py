import datetime
from dataclasses import dataclass, field
from typing import Optional, final

from typing_extensions import TypeAlias

ArticleID: TypeAlias = int
AuthorID: TypeAlias = int


@final
@dataclass(frozen=True)
class NewArticleDetails:
    title: str
    description: str
    body: str
    tags: list[str] = field(default_factory=list)


@final
@dataclass
class ArticleAuthor:
    username: str
    bio: str
    image: Optional[str] = field(default=None)
    following: bool = field(default=False)


@final
@dataclass
class ArticleWithAuthor:
    slug: str
    title: str
    description: str
    body: str
    tags: list[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    author: ArticleAuthor
    favorited: bool = field(default=False)
    favorites_count: int = field(default=0)


@final
@dataclass
class BodylessArticleWithAuthor:
    slug: str
    title: str
    description: str
    tags: list[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    author: ArticleAuthor
    favorited: bool = field(default=False)
    favorites_count: int = field(default=0)


@final
@dataclass
class Article:
    id: ArticleID
    author_id: AuthorID
    title: str
    slug: str
    description: str
    body: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
