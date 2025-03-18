import abc

from conduit.domain.users.user import UserID


class FollowersRepository(abc.ABC):
    @abc.abstractmethod
    async def exists(self, follower_id: UserID, following_id: UserID) -> bool: ...

    @abc.abstractmethod
    async def create(self, follower_id: UserID, following_id: UserID) -> None: ...

    @abc.abstractmethod
    async def delete(self, follower_id: UserID, following_id: UserID) -> None: ...
