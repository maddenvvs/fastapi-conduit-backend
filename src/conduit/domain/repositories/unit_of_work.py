import abc
from typing import AsyncContextManager

from conduit.domain.repositories.tags import ITagsRepository
from conduit.domain.repositories.users import UsersRepository


class UnitOfWorkContext(abc.ABC):

    @property
    @abc.abstractmethod
    def tags(self) -> ITagsRepository: ...

    @property
    @abc.abstractmethod
    def users(self) -> UsersRepository: ...


class UnitOfWork(abc.ABC):

    @abc.abstractmethod
    def begin(self) -> AsyncContextManager[UnitOfWorkContext]: ...
