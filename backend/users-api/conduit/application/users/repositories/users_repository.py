import abc
from typing import Optional

from conduit.domain.entities.users import (
    User,
    UserID,
)


class UsersRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(
        self,
        user_id: UserID,
    ) -> Optional[User]: ...

    @abc.abstractmethod
    async def get_by_email(
        self,
        email: str,
    ) -> Optional[User]: ...

    @abc.abstractmethod
    async def get_by_username(
        self,
        username: str,
    ) -> Optional[User]: ...
