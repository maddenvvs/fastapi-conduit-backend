import abc
from typing import AsyncContextManager

from conduit.domain.repositories.articles import ArticlesRepository
from conduit.domain.repositories.tags import TagsRepository
from conduit.domain.repositories.users import UsersRepository


class UnitOfWorkContext(abc.ABC):

    @property
    @abc.abstractmethod
    def tags(self) -> TagsRepository: ...

    @property
    @abc.abstractmethod
    def users(self) -> UsersRepository: ...

    @property
    @abc.abstractmethod
    def articles(self) -> ArticlesRepository: ...


class UnitOfWork(abc.ABC):

    @abc.abstractmethod
    def begin(self) -> AsyncContextManager[UnitOfWorkContext]: ...
