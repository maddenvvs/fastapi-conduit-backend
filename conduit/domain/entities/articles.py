import datetime
from dataclasses import dataclass
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
    tags: list[str]


@final
@dataclass(frozen=True)
class NewArticleDetailsWithSlug:
    title: str
    slug: str
    description: str
    body: str
    tags: list[str]


@final
@dataclass
class ArticleAuthor:
    username: str
    bio: str
    image: Optional[str]
    following: bool


@final
@dataclass
class ArticleWithAuthor:
    id: ArticleID
    slug: str
    title: str
    description: str
    body: str
    tags: list[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    author: ArticleAuthor
    favorited: bool
    favorites_count: int


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
    favorited: bool
    favorites_count: int


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
