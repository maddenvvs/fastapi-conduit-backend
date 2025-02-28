import abc

from conduit.domain.entities.articles import ArticleID
from conduit.domain.entities.users import UserID


class FavoritesRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, article_id: ArticleID, user_id: UserID) -> None: ...

    @abc.abstractmethod
    async def delete(self, article_id: ArticleID, user_id: UserID) -> None: ...

    @abc.abstractmethod
    async def exists(self, article_id: ArticleID, user_id: UserID) -> bool: ...

    @abc.abstractmethod
    async def count(self, article_id: ArticleID) -> int: ...
