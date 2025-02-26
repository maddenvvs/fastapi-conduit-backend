from datetime import datetime
from typing import Any, AsyncGenerator

import pytest
from fastapi import status
from httpx import AsyncClient, Response
from sqlalchemy import delete

from conduit.infrastructure.persistence.database import Database
from conduit.infrastructure.persistence.models import TagModel


class TestSuccessfullyListTags:

    @pytest.fixture(
        params=[
            [],
            ["tag_a", "tag_b", "tag_c"],
            ["programming", "requirejs"],
            ["z", "x", "y"],
        ]
    )
    async def test_tag_names(self, request: pytest.FixtureRequest) -> Any:
        return request.param

    @pytest.fixture(autouse=True)
    async def create_test_tags(
        self, test_db: Database, test_tag_names: list[str]
    ) -> AsyncGenerator[None, None]:
        async with test_db.create_session() as session:
            session.add_all(
                [
                    TagModel(name=name, created_at=datetime(year=2022, month=2, day=18))
                    for name in test_tag_names
                ]
            )
            await session.commit()
            yield
            await session.execute(delete(TagModel))
            await session.commit()

    class TestForAnyClient:

        @pytest.fixture
        async def tags_response(self, any_client: AsyncClient) -> Response:
            return await any_client.get("/tags")

        @pytest.mark.anyio
        async def test_returns_status_OK(self, tags_response: Response) -> None:
            assert tags_response.status_code == status.HTTP_200_OK

        @pytest.mark.anyio
        async def test_returns_all_available_tags(
            self,
            test_tag_names: list[str],
            tags_response: Response,
        ) -> None:
            assert tags_response.json() == {"tags": test_tag_names}
