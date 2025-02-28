from typing import final

from sqlalchemy import delete, insert, select

from conduit.domain.entities.articles import ArticleID
from conduit.domain.entities.comments import Comment, NewComment
from conduit.domain.repositories.comments import CommentsRepository
from conduit.infrastructure.current_time import CurrentTime
from conduit.infrastructure.persistence.models import CommentModel
from conduit.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork


def _to_domain_comment(comment: CommentModel) -> Comment:
    return Comment(
        id=comment.id,
        author_id=comment.author_id,
        article_id=comment.article_id,
        body=comment.body,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
    )


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
        return _to_domain_comment(created_comment)

    async def list_by_article_id(self, article_id: ArticleID) -> list[Comment]:
        session = SqlAlchemyUnitOfWork.get_current_session()
        query = select(CommentModel).where(CommentModel.article_id == article_id)

        comments = await session.scalars(query)
        return [_to_domain_comment(comment) for comment in comments]

    async def get(self, comment_id: ArticleID) -> Comment:
        session = SqlAlchemyUnitOfWork.get_current_session()
        query = select(CommentModel).where(CommentModel.id == comment_id)
        result = await session.execute(query)
        comment = result.scalar_one()
        return _to_domain_comment(comment)

    async def delete(self, comment_id: ArticleID) -> None:
        session = SqlAlchemyUnitOfWork.get_current_session()
        query = delete(CommentModel).where(CommentModel.id == comment_id)
        await session.execute(query)
