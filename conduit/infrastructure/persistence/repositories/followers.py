from sqlalchemy import delete, exists, insert

from conduit.domain.entities.users import UserID
from conduit.domain.repositories.followers import FollowersRepository
from conduit.infrastructure.persistence.models import FollowerModel
from conduit.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork
from conduit.infrastructure.time import CurrentTime


class SQLiteFollowersRepository(FollowersRepository):
    def __init__(self, now: CurrentTime) -> None:
        self._now = now

    async def exists(self, follower_id: UserID, following_id: UserID) -> bool:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = (
            exists()
            .where(
                FollowerModel.follower_id == follower_id,
                FollowerModel.following_id == following_id,
            )
            .select()
        )

        result = await session.scalar(query)
        return bool(result)

    async def create(self, follower_id: UserID, following_id: UserID) -> None:
        session = SqlAlchemyUnitOfWork.get_current_session()
        current_time = self._now()

        query = insert(FollowerModel).values(
            follower_id=follower_id,
            following_id=following_id,
            created_at=current_time,
        )

        await session.execute(query)

    async def delete(self, follower_id: UserID, following_id: UserID) -> None:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = delete(FollowerModel).where(
            FollowerModel.follower_id == follower_id,
            FollowerModel.following_id == following_id,
        )

        await session.execute(query)
