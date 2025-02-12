import abc
from typing import AsyncContextManager

from conduit.domain.repositories.tags import ITagsRepository


class UnitOfWorkContext(abc.ABC):

    @property
    @abc.abstractmethod
    def tags(self) -> ITagsRepository: ...


class UnitOfWork(abc.ABC):

    @abc.abstractmethod
    def begin(self) -> AsyncContextManager[UnitOfWorkContext]: ...
