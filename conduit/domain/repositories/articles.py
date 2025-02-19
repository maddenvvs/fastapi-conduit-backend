import abc
from typing import Optional

from conduit.domain.entities.articles import (
    Article,
    AuthorID,
    BodylessArticleWithAuthor,
    NewArticleDetailsWithSlug,
)
from conduit.domain.entities.users import UserID


class ArticlesRepository(abc.ABC):

    @abc.abstractmethod
    async def get_by_slug_or_none(self, slug: str) -> Optional[Article]: ...

    @abc.abstractmethod
    async def add(
        self, author_id: AuthorID, article_details: NewArticleDetailsWithSlug
    ) -> Article: ...

    @abc.abstractmethod
    async def list_by_followings(
        self, user_id: UserID, limit: int, offset: int
    ) -> list[BodylessArticleWithAuthor]: ...

    @abc.abstractmethod
    async def count_by_followings(self, user_id: UserID) -> int: ...
