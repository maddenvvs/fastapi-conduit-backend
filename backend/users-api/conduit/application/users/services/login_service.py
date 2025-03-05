import abc

from returns.maybe import Maybe

from conduit.domain.users.user import User


class LoginService(abc.ABC):
    @abc.abstractmethod
    async def login(self, email: str, password: str) -> Maybe[User]: ...
