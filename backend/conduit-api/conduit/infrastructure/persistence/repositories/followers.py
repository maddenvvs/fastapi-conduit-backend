from sqlalchemy import delete, exists, insert, select

from conduit.application.common.repositories.followers import FollowersRepository
from conduit.domain.users.user import UserID
from conduit.infrastructure.persistence.models import FollowerModel
from conduit.shared.infrastructure.current_time import CurrentTime
from conduit.shared.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork


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

    async def list(self, follower_id: UserID, following_ids: list[int]) -> list[int]:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = select(FollowerModel.following_id).where(
            FollowerModel.following_id.in_(following_ids),
            FollowerModel.follower_id == follower_id,
        )

        result = await session.execute(query)
        return list(result.scalars())
