import abc
from dataclasses import dataclass
from typing import Optional, final

from conduit.domain.articles.articles import (
    Article,
    ArticleID,
    AuthorID,
    BodylessArticleWithAuthor,
    NewArticleDetailsWithSlug,
    UpdateArticleFields,
)
from conduit.domain.users.user import UserID


@final
@dataclass(frozen=True)
class ListFilters:
    tag: Optional[str]
    author: Optional[str]
    favorited: Optional[str]


class ArticlesRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_slug_or_none(self, slug: str) -> Optional[Article]: ...

    @abc.abstractmethod
    async def add(
        self,
        author_id: AuthorID,
        article_details: NewArticleDetailsWithSlug,
    ) -> Article: ...

    @abc.abstractmethod
    async def list_by_followings(
        self,
        user_id: UserID,
        limit: int,
        offset: int,
    ) -> list[BodylessArticleWithAuthor]: ...

    @abc.abstractmethod
    async def count_by_followings(self, user_id: UserID) -> int: ...

    @abc.abstractmethod
    async def list_by_filters(
        self,
        user_id: Optional[UserID],
        limit: int,
        offset: int,
        filters: ListFilters,
    ) -> list[BodylessArticleWithAuthor]: ...

    @abc.abstractmethod
    async def count_by_filters(
        self,
        tag: Optional[str],
        author: Optional[str],
        favorited: Optional[str],
    ) -> int: ...

    @abc.abstractmethod
    async def delete_by_id(self, article_id: ArticleID) -> None: ...

    @abc.abstractmethod
    async def update_by_slug(
        self,
        slug: str,
        update_fields: UpdateArticleFields,
    ) -> Article: ...
