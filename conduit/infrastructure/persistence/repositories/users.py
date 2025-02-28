from typing import Optional, final

from sqlalchemy import insert, select, update

from conduit.domain.entities.users import (
    CreateUserDetails,
    UpdateUserDetails,
    User,
    UserID,
)
from conduit.domain.repositories.users import UsersRepository
from conduit.infrastructure.persistence.models import UserModel
from conduit.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork
from conduit.infrastructure.time import CurrentTime


def _model_to_entity(model: UserModel) -> User:
    return User(
        id=model.id,
        email=model.email,
        username=model.username,
        bio=model.bio,
        image=model.image_url,
        password_hash=model.password_hash,
    )


@final
class SQLiteUsersRepository(UsersRepository):
    def __init__(
        self,
        now: CurrentTime,
    ) -> None:
        self._now = now

    async def get_by_id_or_none(self, id: UserID) -> Optional[User]:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = select(UserModel).where(UserModel.id == id)
        if user := await session.scalar(query):
            return _model_to_entity(user)
        return None

    async def get_by_email_or_none(self, email: str) -> Optional[User]:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = select(UserModel).where(UserModel.email == email)
        if user := await session.scalar(query):
            return _model_to_entity(user)
        return None

    async def get_by_username_or_none(self, username: str) -> Optional[User]:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = select(UserModel).where(UserModel.username == username)
        if user := await session.scalar(query):
            return _model_to_entity(user)
        return None

    async def add(self, user_details: CreateUserDetails) -> User:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = (
            insert(UserModel)
            .values(
                username=user_details.username,
                email=user_details.email,
                password_hash=user_details.password_hash,
                bio="",
                created_at=self._now(),
            )
            .returning(UserModel)
        )
        result = await session.execute(query)
        user = result.scalar_one()
        return _model_to_entity(user)

    async def update(self, user_id: UserID, update_details: UpdateUserDetails) -> User:
        session = SqlAlchemyUnitOfWork.get_current_session()

        current_time = self._now()
        query = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(updated_at=current_time)
            .returning(UserModel)
        )

        if update_details.username is not None:
            query = query.values(username=update_details.username)

        if update_details.email is not None:
            query = query.values(email=update_details.email)

        if update_details.password_hash is not None:
            query = query.values(password_hash=update_details.password_hash)

        if update_details.bio is not None:
            query = query.values(bio=update_details.bio)

        if update_details.image_url is not None:
            query = query.values(image_url=update_details.image_url)

        result = await session.execute(query)
        updated_user = result.scalar_one()
        return _model_to_entity(updated_user)

    async def list_by_user_ids(self, user_ids: list[int]) -> list[User]:
        session = SqlAlchemyUnitOfWork.get_current_session()

        query = select(UserModel).where(UserModel.id.in_(user_ids))
        users = await session.scalars(query)
        return [_model_to_entity(user) for user in users]
