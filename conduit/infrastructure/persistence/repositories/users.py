from typing import Optional, final

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from conduit.domain.entities.users import (
    CreateUserDetails,
    UpdateUserDetails,
    User,
    UserID,
)
from conduit.domain.repositories.users import UsersRepository
from conduit.infrastructure.persistence.models import UserModel
from conduit.infrastructure.time import CurrentTime


def model_to_entity(model: UserModel) -> User:
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
        session: AsyncSession,
        now: CurrentTime,
    ) -> None:
        self._session = session
        self._now = now

    async def get_by_id_or_none(self, id: UserID) -> Optional[User]:
        query = select(UserModel).where(UserModel.id == id)
        if user := await self._session.scalar(query):
            return model_to_entity(user)
        return None

    async def get_by_email_or_none(self, email: str) -> Optional[User]:
        query = select(UserModel).where(UserModel.email == email)
        if user := await self._session.scalar(query):
            return model_to_entity(user)
        return None

    async def get_by_username_or_none(self, username: str) -> Optional[User]:
        query = select(UserModel).where(UserModel.username == username)
        if user := await self._session.scalar(query):
            return model_to_entity(user)
        return None

    async def add(self, user_details: CreateUserDetails) -> User:
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
        result = await self._session.execute(query)
        user = result.scalar_one()
        return model_to_entity(user)

    async def update(self, user_id: UserID, update_details: UpdateUserDetails) -> User:
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

        result = await self._session.execute(query)
        updated_user = result.scalar_one()
        return model_to_entity(updated_user)
