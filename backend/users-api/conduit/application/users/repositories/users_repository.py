import abc

from returns.maybe import Maybe

from conduit.domain.users.new_user import NewUser
from conduit.domain.users.updated_user import UpdatedUser
from conduit.domain.users.user import User, UserId


class UsersRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, user_id: UserId) -> Maybe[User]: ...

    @abc.abstractmethod
    async def get_by_email(self, email: str) -> Maybe[User]: ...

    @abc.abstractmethod
    async def get_by_username(self, username: str) -> Maybe[User]: ...

    @abc.abstractmethod
    async def create(self, new_user: NewUser) -> User: ...

    @abc.abstractmethod
    async def update(self, updated_user: UpdatedUser) -> User: ...
