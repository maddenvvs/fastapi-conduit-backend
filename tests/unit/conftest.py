import contextlib
import unittest.mock as mock
from typing import Any, AsyncIterator

import pytest

from conduit.domain.repositories.tags import ITagsRepository
from conduit.domain.repositories.unit_of_work import UnitOfWork, UnitOfWorkContext
from conduit.domain.repositories.users import UsersRepository


@pytest.fixture
def tags_repository() -> Any:
    return mock.create_autospec(spec=ITagsRepository, spec_set=True)


@pytest.fixture
def users_repository() -> Any:
    return mock.create_autospec(spec=UsersRepository, spec_set=True)


class FakeUnitOfWork(UnitOfWork):

    class Context(UnitOfWorkContext):

        def __init__(self, tags: ITagsRepository, users: UsersRepository) -> None:
            self._tags = tags
            self._users = users

        @property
        def tags(self) -> ITagsRepository:
            return self._tags

        @property
        def users(self) -> UsersRepository:
            return self._users

    def __init__(
        self,
        tags: ITagsRepository,
        users: UsersRepository,
    ):
        self._tags = tags
        self._users = users

    @contextlib.asynccontextmanager
    async def begin(self) -> AsyncIterator[UnitOfWorkContext]:
        yield self.Context(tags=self._tags, users=self._users)


@pytest.fixture
def unit_of_work(
    tags_repository: ITagsRepository,
    users_repository: UsersRepository,
) -> FakeUnitOfWork:
    return FakeUnitOfWork(
        tags=tags_repository,
        users=users_repository,
    )
