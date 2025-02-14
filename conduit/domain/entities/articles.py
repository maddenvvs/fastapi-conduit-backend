import datetime
from dataclasses import dataclass


@dataclass
class ArticleAuthor:
    username: str
    bio: str
    image: str
    following: bool


@dataclass
class Article:
    slug: str
    title: str
    description: str
    body: str
    tags: list[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    favorited: bool
    favorites_count: int
    author: ArticleAuthor
