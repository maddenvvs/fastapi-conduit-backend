from typing import final

from returns.maybe import Maybe, Nothing, Some
from sqlalchemy import insert, select, update

from conduit.application.users.repositories.users_repository import UsersRepository
from conduit.domain.users.new_user import NewUser
from conduit.domain.users.updated_user import UpdatedUser
from conduit.domain.users.user import (
    User,
    UserId,
)
from conduit.infrastructure.common.current_time import CurrentTime
from conduit.infrastructure.common.persistence.models import UserModel
from conduit.infrastructure.common.persistence.unit_of_work import SqlAlchemyUnitOfWork
from conduit.infrastructure.users.services.password_service import PasswordHasher


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
        if user_model := await session.scalar(query):
            return Some(user_model.to_user())
        return Nothing

    async def get_by_email(self, email: str) -> Maybe[User]:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = select(UserModel).where(UserModel.email == email)
        if user_model := await session.scalar(query):
            return Some(user_model.to_user())
        return Nothing

    async def get_by_username(self, username: str) -> Maybe[User]:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = select(UserModel).where(UserModel.username == username)
        if user_model := await session.scalar(query):
            return Some(user_model.to_user())
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
        user_model = result.scalar_one()
        return user_model.to_user()

    async def update(self, updated_user: UpdatedUser) -> User:
        session = SqlAlchemyUnitOfWork.get_current_session()

        current_time = self._now()
        query = (
            update(UserModel)
            .where(UserModel.id == updated_user.id)
            .values(updated_at=current_time)
            .returning(UserModel)
        )

        if updated_user.username is not None:
            query = query.values(username=updated_user.username)

        if updated_user.email is not None:
            query = query.values(email=updated_user.email)

        if updated_user.password is not None:
            password_hash = self._password_hasher(updated_user.password)
            query = query.values(password_hash=password_hash)

        if updated_user.bio is not None:
            query = query.values(bio=updated_user.bio)

        if updated_user.image_url is not None:
            query = query.values(image_url=updated_user.image_url)

        result = await session.execute(query)
        user_model = result.scalar_one()
        return user_model.to_user()
