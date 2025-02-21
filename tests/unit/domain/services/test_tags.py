import logging
import unittest.mock as mock
from typing import Any

import pytest

from conduit.domain.entities.tags import Tag
from conduit.domain.repositories.tags import TagsRepository
from conduit.domain.services.tags_service import TagsService


@pytest.fixture
def tags_service_logger() -> Any:
    return mock.create_autospec(spec=logging.Logger, spec_set=True)


@pytest.fixture
def tags_service(
    tags_repository: TagsRepository,
    tags_service_logger: logging.Logger,
) -> TagsService:
    return TagsService(
        tags_repository=tags_repository,
        logger=tags_service_logger,
    )


class TestSuccessullyGetAllTags:

    @pytest.fixture(
        autouse=True,
        params=[
            [
                Tag(id=1, name="angularjs"),
            ],
            [
                Tag(id=2, name="reactjs"),
                Tag(id=4, name="angularjs"),
                Tag(id=7, name="python"),
            ],
        ],
    )
    async def returned_tags(
        self,
        request: pytest.FixtureRequest,
        tags_repository: mock.AsyncMock,
    ) -> None:
        tags_repository.get_all_tags.return_value = request.param

    @pytest.mark.anyio
    async def test_returns_tags(self, tags_service: TagsService) -> None:
        returned_tags = await tags_service.get_all_tags()

        assert len(returned_tags) > 0

    @pytest.mark.anyio
    async def test_tags_repository_was_invoked(
        self,
        tags_service: TagsService,
        tags_repository: mock.AsyncMock,
    ) -> None:
        await tags_service.get_all_tags()

        tags_repository.get_all_tags.assert_awaited_once()

    @pytest.mark.anyio
    async def test_logs_the_initial_message(
        self,
        tags_service: TagsService,
        tags_service_logger: mock.Mock,
    ) -> None:
        await tags_service.get_all_tags()

        tags_service_logger.info.assert_any_call("Retrieving tags")

    @pytest.mark.anyio
    async def test_logs_the_final_message_with_time(
        self,
        tags_service: TagsService,
        tags_service_logger: mock.Mock,
    ) -> None:
        await tags_service.get_all_tags()

        tags_service_logger.info.assert_any_call(
            "Retrieving tags took %dms",
            mock.ANY,
            extra=mock.ANY,
        )


class TestRepositoryRaisesException:

    class CustomException(Exception):
        pass

    @pytest.fixture(autouse=True)
    def failed_repository(self, tags_repository: Any) -> None:
        tags_repository.get_all_tags.side_effect = (
            TestRepositoryRaisesException.CustomException("Something went wrong")
        )

    @pytest.mark.anyio
    async def test_tags_service_reraises_exception(
        self,
        tags_service: TagsService,
    ) -> None:
        with pytest.raises(TestRepositoryRaisesException.CustomException):
            await tags_service.get_all_tags()

    @pytest.mark.anyio
    async def test_tags_repository_was_invoked(
        self,
        tags_repository: mock.AsyncMock,
        tags_service: TagsService,
    ) -> None:
        with pytest.raises(TestRepositoryRaisesException.CustomException):
            await tags_service.get_all_tags()

        tags_repository.get_all_tags.assert_awaited_once()

    @pytest.mark.anyio
    async def test_logs_the_initial_message(
        self,
        tags_service: TagsService,
        tags_service_logger: mock.Mock,
    ) -> None:
        with pytest.raises(TestRepositoryRaisesException.CustomException):
            await tags_service.get_all_tags()

        tags_service_logger.info.assert_any_call("Retrieving tags")

    @pytest.mark.anyio
    async def test_tags_service_logger_logs_error(
        self,
        tags_service: TagsService,
        tags_service_logger: mock.AsyncMock,
    ) -> None:
        with pytest.raises(TestRepositoryRaisesException.CustomException):
            await tags_service.get_all_tags()

        tags_service_logger.error.assert_called_once_with(
            "Error retrieving tags",
            extra=mock.ANY,
        )
