from typing import Any
from unittest import mock

import pytest

from conduit.application.common.repositories.articles import ArticlesRepository
from conduit.application.common.repositories.followers import FollowersRepository
from conduit.application.common.repositories.tags import TagsRepository
from conduit.application.common.repositories.users import UsersRepository


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
