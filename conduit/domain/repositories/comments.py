import abc

from conduit.domain.entities.comments import Comment, NewComment


class CommentsRepository(abc.ABC):

    @abc.abstractmethod
    async def add(self, new_comment: NewComment) -> Comment: ...
