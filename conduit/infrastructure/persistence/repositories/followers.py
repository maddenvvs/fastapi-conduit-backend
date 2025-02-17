from sqlalchemy import delete, exists, insert
from sqlalchemy.ext.asyncio import AsyncSession

from conduit.domain.entities.users import UserID
from conduit.domain.repositories.followers import FollowersRepository
from conduit.infrastructure.persistence.models import FollowerModel
from conduit.infrastructure.time import CurrentTime


class SQLiteFollowersRepository(FollowersRepository):

    def __init__(self, session: AsyncSession, now: CurrentTime) -> None:
        self._session = session
        self._now = now

    async def exists(self, follower_id: UserID, following_id: UserID) -> bool:
        query = (
            exists()
            .where(
                FollowerModel.follower_id == follower_id,
                FollowerModel.following_id == following_id,
            )
            .select()
        )

        result = await self._session.scalar(query)
        return bool(result)

    async def create(self, follower_id: UserID, following_id: UserID) -> None:
        current_time = self._now()

        query = insert(FollowerModel).values(
            follower_id=follower_id,
            following_id=following_id,
            created_at=current_time,
        )

        await self._session.execute(query)

    async def delete(self, follower_id: UserID, following_id: UserID) -> None:
        query = delete(FollowerModel).where(
            FollowerModel.follower_id == follower_id,
            FollowerModel.following_id == following_id,
        )

        await self._session.execute(query)
