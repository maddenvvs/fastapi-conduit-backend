from sqlalchemy import delete, exists, insert, select
from sqlalchemy.sql.functions import count

from conduit.application.common.repositories.favorites import FavoritesRepository
from conduit.domain.entities.articles import ArticleID
from conduit.domain.entities.users import UserID
from conduit.infrastructure.persistence.models import FavoriteModel
from conduit.shared.infrastructure.current_time import CurrentTime
from conduit.shared.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork


class SQLiteFavoritesRepository(FavoritesRepository):
    def __init__(self, now: CurrentTime) -> None:
        self._now = now

    async def add(self, article_id: UserID, user_id: ArticleID) -> None:
        session = SqlAlchemyUnitOfWork.get_current_session()
        current_time = self._now()

        query = insert(FavoriteModel).values(
            article_id=article_id,
            user_id=user_id,
            created_at=current_time,
        )

        await session.execute(query)

    async def delete(self, article_id: ArticleID, user_id: ArticleID) -> None:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = delete(FavoriteModel).where(
            FavoriteModel.article_id == article_id,
            FavoriteModel.user_id == user_id,
        )

        await session.execute(query)

    async def exists(self, article_id: ArticleID, user_id: ArticleID) -> bool:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = (
            exists()
            .where(
                FavoriteModel.article_id == article_id,
                FavoriteModel.user_id == user_id,
            )
            .select()
        )

        result = await session.execute(query)
        return result.scalar_one()

    async def count(self, article_id: ArticleID) -> int:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = select(count()).where(FavoriteModel.article_id == article_id)

        result = await session.execute(query)
        return result.scalar_one()
