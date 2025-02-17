import contextlib
import unittest.mock as mock
from typing import Any, AsyncIterator

import pytest

from conduit.domain.repositories.articles import ArticlesRepository
from conduit.domain.repositories.followers import FollowersRepository
from conduit.domain.repositories.tags import TagsRepository
from conduit.domain.repositories.unit_of_work import UnitOfWork, UnitOfWorkContext
from conduit.domain.repositories.users import UsersRepository


@pytest.fixture
def tags_repository() -> Any:
    return mock.create_autospec(spec=TagsRepository, spec_set=True)


@pytest.fixture
def users_repository() -> Any:
    return mock.create_autospec(spec=UsersRepository, spec_set=True)


@pytest.fixture
def articles_repository() -> Any:
    return mock.create_autospec(spec=ArticlesRepository, spec_set=True)


@pytest.fixture
def followers_repository() -> Any:
    return mock.create_autospec(spec=FollowersRepository, spec_set=True)


class FakeUnitOfWork(UnitOfWork):

    class Context(UnitOfWorkContext):

        def __init__(
            self,
            tags: TagsRepository,
            users: UsersRepository,
            articles: ArticlesRepository,
            followers: FollowersRepository,
        ) -> None:
            self._tags = tags
            self._users = users
            self._articles = articles
            self._followers = followers

        @property
        def tags(self) -> TagsRepository:
            return self._tags

        @property
        def users(self) -> UsersRepository:
            return self._users

        @property
        def articles(self) -> ArticlesRepository:
            return self._articles

        @property
        def followers(self) -> FollowersRepository:
            return self._followers

    def __init__(
        self,
        tags: TagsRepository,
        users: UsersRepository,
        articles: ArticlesRepository,
        followers: FollowersRepository,
    ):
        self._tags = tags
        self._users = users
        self._articles = articles
        self._followers = followers

    @contextlib.asynccontextmanager
    async def begin(self) -> AsyncIterator[UnitOfWorkContext]:
        yield self.Context(
            tags=self._tags,
            users=self._users,
            articles=self._articles,
            followers=self._followers,
        )


@pytest.fixture
def unit_of_work(
    tags_repository: TagsRepository,
    users_repository: UsersRepository,
    articles_repository: ArticlesRepository,
    followers_repository: FollowersRepository,
) -> FakeUnitOfWork:
    return FakeUnitOfWork(
        tags=tags_repository,
        users=users_repository,
        articles=articles_repository,
        followers=followers_repository,
    )
