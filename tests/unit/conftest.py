import unittest.mock as mock
from typing import Any

import pytest

from conduit.domain.repositories.articles import ArticlesRepository
from conduit.domain.repositories.followers import FollowersRepository
from conduit.domain.repositories.tags import TagsRepository
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
