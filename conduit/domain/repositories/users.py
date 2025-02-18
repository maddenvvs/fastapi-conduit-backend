import abc
from typing import Optional

from conduit.domain.entities.users import (
    CreateUserDetails,
    UpdateUserDetails,
    User,
    UserID,
)


class UsersRepository(abc.ABC):

    @abc.abstractmethod
    async def get_by_id_or_none(
        self,
        id: UserID,
    ) -> Optional[User]: ...

    @abc.abstractmethod
    async def get_by_email_or_none(
        self,
        email: str,
    ) -> Optional[User]: ...

    @abc.abstractmethod
    async def get_by_username_or_none(
        self,
        username: str,
    ) -> Optional[User]: ...

    @abc.abstractmethod
    async def add(
        self,
        user_details: CreateUserDetails,
    ) -> User: ...

    @abc.abstractmethod
    async def update(
        self,
        user_id: UserID,
        update_details: UpdateUserDetails,
    ) -> User: ...
