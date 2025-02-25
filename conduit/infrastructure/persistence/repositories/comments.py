from typing import final

from sqlalchemy import insert

from conduit.domain.entities.comments import Comment, NewComment
from conduit.domain.repositories.comments import CommentsRepository
from conduit.infrastructure.persistence.models import CommentModel
from conduit.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork
from conduit.infrastructure.time import CurrentTime


@final
class SQLiteCommentsRepository(CommentsRepository):

    def __init__(self, now: CurrentTime) -> None:
        self._now = now

    async def add(self, new_comment: NewComment) -> Comment:
        session = SqlAlchemyUnitOfWork.get_current_session()
        current_time = self._now()

        query = (
            insert(CommentModel)
            .values(
                author_id=new_comment.author_id,
                article_id=new_comment.article_id,
                body=new_comment.body,
                created_at=current_time,
                updated_at=current_time,
            )
            .returning(CommentModel)
        )

        result = await session.execute(query)
        created_comment = result.scalar_one()

        return Comment(
            id=created_comment.id,
            author_id=created_comment.author_id,
            article_id=created_comment.article_id,
            body=created_comment.body,
            created_at=created_comment.created_at,
            updated_at=created_comment.updated_at,
        )
