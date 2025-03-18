from typing import Optional, final
from uuid import UUID

from sqlalchemy import select

from conduit.application.common.repositories.users import UsersRepository
from conduit.domain.entities.users import (
    User,
    UserID,
)
from conduit.infrastructure.persistence.models import UserModel
from conduit.shared.infrastructure.current_time import CurrentTime
from conduit.shared.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork


@final
class SQLiteUsersRepository(UsersRepository):
    def __init__(
        self,
        now: CurrentTime,
    ) -> None:
        self._now = now

    async def get_by_id_or_none(self, user_id: UserID) -> Optional[User]:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = select(UserModel).where(UserModel.id == user_id)
        if user_model := await session.scalar(query):
            return user_model.to_user()
        return None

    async def get_by_user_id_or_none(self, user_id: UUID) -> Optional[User]:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = select(UserModel).where(UserModel.user_id == user_id)
        if user_model := await session.scalar(query):
            return user_model.to_user()
        return None

    async def get_by_username_or_none(self, username: str) -> Optional[User]:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = select(UserModel).where(UserModel.username == username)
        if user_model := await session.scalar(query):
            return user_model.to_user()
        return None

    async def list_by_user_ids(self, user_ids: list[int]) -> list[User]:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = select(UserModel).where(UserModel.id.in_(user_ids))
        users = await session.scalars(query)
        return [user.to_user() for user in users]
