from typing import final

from returns.maybe import Maybe, Nothing, Some
from sqlalchemy import insert, select

from conduit.application.users.repositories.users_repository import UsersRepository
from conduit.domain.users.new_user import NewUser
from conduit.domain.users.user import (
    User,
    UserId,
)
from conduit.infrastructure.common.current_time import CurrentTime
from conduit.infrastructure.common.persistence.models import UserModel
from conduit.infrastructure.common.persistence.unit_of_work import SqlAlchemyUnitOfWork
from conduit.infrastructure.users.services.password_service import PasswordHasher


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
        password_hasher: PasswordHasher,
    ) -> None:
        self._now = now
        self._password_hasher = password_hasher

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

    async def create(self, new_user: NewUser) -> User:
        session = SqlAlchemyUnitOfWork.get_current_session()

        password_hash = self._password_hasher(new_user.password)
        query = (
            insert(UserModel)
            .values(
                username=new_user.username,
                email=new_user.email,
                password_hash=password_hash,
                bio="",
                created_at=self._now(),
                updated_at=self._now(),
            )
            .returning(UserModel)
        )
        result = await session.execute(query)
        user = result.scalar_one()
        return _model_to_entity(user)
