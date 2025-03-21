import abc

from conduit.domain.articles.articles import ArticleID
from conduit.domain.tags.tag import Tag


class TagsRepository(abc.ABC):
    @abc.abstractmethod
    async def get_all_tags(self) -> list[Tag]: ...

    @abc.abstractmethod
    async def add_many(self, article_id: ArticleID, tags: list[str]) -> list[Tag]: ...

    @abc.abstractmethod
    async def list_by_article_id(self, article_id: ArticleID) -> list[Tag]: ...
