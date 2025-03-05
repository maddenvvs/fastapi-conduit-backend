from typing import final

from returns.maybe import Maybe, Nothing, Some
from sqlalchemy import select

from conduit.application.users.services.login_service import LoginService
from conduit.domain.users.user import User
from conduit.infrastructure.common.persistence.models import UserModel
from conduit.infrastructure.common.persistence.unit_of_work import SqlAlchemyUnitOfWork
from conduit.infrastructure.users.services.password_service import PasswordHasher


@final
class SQLiteLoginService(LoginService):
    def __init__(self, password_hasher: PasswordHasher) -> None:
        self._password_hasher = password_hasher

    async def login(self, email: str, password: str) -> Maybe[User]:
        session = SqlAlchemyUnitOfWork.get_current_session()

        password_hash = self._password_hasher(password)
        query = select(UserModel).where(
            UserModel.email == email,
            UserModel.password_hash == password_hash,
        )
        if user_model := await session.scalar(query):
            return Some(user_model.to_user())
        return Nothing
