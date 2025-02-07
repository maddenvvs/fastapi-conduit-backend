import abc
from typing import Optional

from conduit.domain.entities.articles import Article


class IArticlesRepository(abc.ABC):

    @abc.abstractmethod
    async def find_article_by_slug(self, slug: str) -> Optional[Article]: ...
