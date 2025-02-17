import abc
from typing import Optional

from conduit.domain.entities.articles import Article, AuthorID, NewArticleDetails


class ArticlesRepository(abc.ABC):

    @abc.abstractmethod
    async def get_by_slug_or_none(self, slug: str) -> Optional[Article]: ...

    @abc.abstractmethod
    async def add(
        self, author_id: AuthorID, article_details: NewArticleDetails
    ) -> Article: ...
