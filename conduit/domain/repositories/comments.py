import abc

from conduit.domain.entities.articles import ArticleID
from conduit.domain.entities.comments import Comment, CommentID, NewComment


class CommentsRepository(abc.ABC):

    @abc.abstractmethod
    async def get(self, comment_id: CommentID) -> Comment: ...

    @abc.abstractmethod
    async def delete(self, comment_id: CommentID) -> None: ...

    @abc.abstractmethod
    async def add(self, new_comment: NewComment) -> Comment: ...

    @abc.abstractmethod
    async def list_by_article_id(self, article_id: ArticleID) -> list[Comment]: ...
