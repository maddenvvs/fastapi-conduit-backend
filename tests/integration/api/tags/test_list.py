from datetime import datetime
from typing import Any

import pytest
from fastapi import status
from httpx import AsyncClient, Response

from conduit.infrastructure.persistence.models import TagModel
from tests.integration.conftest import AddToDb


class TestSuccessfullyListTags:
    @pytest.fixture(
        params=[
            [],
            ["tag_a", "tag_b", "tag_c"],
            ["programming", "requirejs"],
            ["z", "x", "y"],
        ],
    )
    async def test_tag_names(self, request: pytest.FixtureRequest) -> Any:
        return request.param

    @pytest.fixture
    async def test_tags(self, test_tag_names: list[str]) -> list[TagModel]:
        return [
            TagModel(
                name=name,
                created_at=datetime(year=2022, month=2, day=18),
            )
            for name in test_tag_names
        ]

    @pytest.fixture(autouse=True)
    async def create_test_tags(
        self,
        test_tags: list[TagModel],
        add_to_db: AddToDb,
    ) -> None:
        await add_to_db(*test_tags)

    class TestForAnyClient:
        @pytest.fixture
        async def tags_response(self, any_client: AsyncClient) -> Response:
            return await any_client.get("/tags")

        @pytest.mark.anyio
        async def test_returns_status_200_ok(self, tags_response: Response) -> None:
            assert tags_response.status_code == status.HTTP_200_OK

        @pytest.mark.anyio
        async def test_returns_all_available_tags(
            self,
            test_tag_names: list[str],
            tags_response: Response,
        ) -> None:
            assert tags_response.json() == {"tags": test_tag_names}
