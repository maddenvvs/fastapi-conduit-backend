import abc
import uuid
from typing import Optional

from conduit.domain.entities.users import (
    User,
    UserID,
)


class UsersRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_id_or_none(
        self,
        user_id: UserID,
    ) -> Optional[User]: ...

    @abc.abstractmethod
    async def get_by_user_id_or_none(
        self,
        user_id: uuid.UUID,
    ) -> Optional[User]: ...

    @abc.abstractmethod
    async def get_by_username_or_none(
        self,
        username: str,
    ) -> Optional[User]: ...

    @abc.abstractmethod
    async def list_by_user_ids(self, user_ids: list[UserID]) -> list[User]: ...
