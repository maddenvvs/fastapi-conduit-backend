from typing import final

from returns.maybe import Maybe, Nothing, Some
from sqlalchemy import select

from conduit.application.users.repositories.users_repository import UsersRepository
from conduit.domain.users.user import (
    User,
    UserId,
)
from conduit.infrastructure.common.current_time import CurrentTime
from conduit.infrastructure.common.persistence.models import UserModel
from conduit.infrastructure.common.persistence.unit_of_work import SqlAlchemyUnitOfWork


def _model_to_entity(model: UserModel) -> User:
    return User(
        id=model.id,
        email=model.email,
        username=model.username,
        bio=model.bio,
        image_url=model.image_url,
    )


@final
class SQLiteUsersRepository(UsersRepository):
    def __init__(
        self,
        now: CurrentTime,
    ) -> None:
        self._now = now

    async def get_by_id(self, user_id: UserId) -> Maybe[User]:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = select(UserModel).where(UserModel.id == user_id)
        if user := await session.scalar(query):
            return Some(_model_to_entity(user))
        return Nothing

    async def get_by_email(self, email: str) -> Maybe[User]:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = select(UserModel).where(UserModel.email == email)
        if user := await session.scalar(query):
            return Some(_model_to_entity(user))
        return Nothing

    async def get_by_username(self, username: str) -> Maybe[User]:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = select(UserModel).where(UserModel.username == username)
        if user := await session.scalar(query):
            return Some(_model_to_entity(user))
        return Nothing
