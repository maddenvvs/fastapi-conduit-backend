import unittest.mock as mock

import pytest

from conduit.domain.repositories.tags import ITagsRepository
from conduit.domain.services.tags import TagsService


@pytest.fixture
def tags_repository() -> mock.AsyncMock:
    return mock.create_autospec(spec=ITagsRepository, spec_set=True)


@pytest.fixture
def tags_service(tags_repository: ITagsRepository) -> TagsService:
    return TagsService(tags_repository)


@pytest.mark.anyio
async def test_tags_service_returns_tags_when_tags_repository_has_them(
    tags_service: TagsService,
    tags_repository: mock.AsyncMock,
):
    tags_repository.get_all_tags.return_value = []

    tags = await tags_service.get_all_tags()

    tags_repository.get_all_tags.assert_awaited_once()
    assert len(tags) == 0


@pytest.mark.anyio
async def test_tags_service_reraises_when_tags_repository_raises_exception(
    tags_service: TagsService,
    tags_repository: mock.AsyncMock,
):
    tags_repository.get_all_tags.side_effect = Exception("Something went wrong")

    with pytest.raises(Exception, match=r"Something went wrong"):
        await tags_service.get_all_tags()
