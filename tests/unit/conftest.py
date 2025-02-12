import contextlib
import unittest.mock as mock
from typing import AsyncIterator

import pytest

from conduit.domain.repositories.tags import ITagsRepository
from conduit.domain.repositories.unit_of_work import UnitOfWork, UnitOfWorkContext


@pytest.fixture
def tags_repository() -> mock.AsyncMock:
    return mock.create_autospec(spec=ITagsRepository, spec_set=True)


class FakeUnitOfWork(UnitOfWork):

    class Context(UnitOfWorkContext):

        def __init__(self, tags: ITagsRepository) -> None:
            self._tags = tags

        @property
        def tags(self) -> ITagsRepository:
            return self._tags

    def __init__(self, tags: ITagsRepository):
        self._tags = tags

    @contextlib.asynccontextmanager
    async def begin(self) -> AsyncIterator[UnitOfWorkContext]:
        yield self.Context(
            tags=self._tags,
        )


@pytest.fixture
def unit_of_work(tags_repository: ITagsRepository):
    return FakeUnitOfWork(
        tags=tags_repository,
    )
