from typing import Optional, final

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from conduit.domain.entities.users import CreateUserDetails, User
from conduit.domain.repositories.users import UsersRepository
from conduit.persistence.models import UserModel
from conduit.time import CurrentTime


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

    async def get_by_email_or_none(self, email: str) -> Optional[User]:
        query = select(UserModel).where(UserModel.email == email)
        if user := await self._session.scalar(query):
            return model_to_entity(user)

    async def get_by_username_or_none(self, username: str) -> Optional[User]:
        query = select(UserModel).where(UserModel.username == username)
        if user := await self._session.scalar(query):
            return model_to_entity(user)

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
