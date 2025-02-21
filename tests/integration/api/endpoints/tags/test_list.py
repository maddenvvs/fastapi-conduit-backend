from datetime import datetime
from typing import Any, AsyncGenerator

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import delete

from conduit.infrastructure.persistence.database import Database
from conduit.infrastructure.persistence.models import TagModel


class TestSuccessfullyListTags:

    @pytest.fixture(
        params=[
            [],
            ["tag_a", "tag_b", "tag_c"],
            ["programming", "requirejs"],
        ]
    )
    async def available_tags(self, request: pytest.FixtureRequest) -> Any:
        return request.param

    @pytest.fixture(autouse=True)
    async def create_tags(
        self, test_db: Database, available_tags: list[str]
    ) -> AsyncGenerator[None, None]:
        async with test_db.create_session() as session:
            session.add_all(
                [
                    TagModel(name=name, created_at=datetime(year=2022, month=2, day=18))
                    for name in available_tags
                ]
            )
            await session.commit()
            yield
            await session.execute(delete(TagModel))
            await session.commit()

    class TestForAnonymousUser:

        @pytest.mark.anyio
        async def test_returns_status_OK(
            self,
            anonymous_test_client: AsyncClient,
        ) -> None:
            response = await anonymous_test_client.get("/tags")

            assert response.status_code == status.HTTP_200_OK

        @pytest.mark.anyio
        async def test_returns_all_available_tags(
            self,
            available_tags: list[str],
            anonymous_test_client: AsyncClient,
        ) -> None:
            response = await anonymous_test_client.get("/tags")

            assert response.json() == {"tags": available_tags}

    class TestForRegisteredUser:

        @pytest.mark.anyio
        async def test_returns_status_OK(
            self,
            registered_user_client: AsyncClient,
        ) -> None:
            response = await registered_user_client.get("/tags")

            assert response.status_code == status.HTTP_200_OK

        @pytest.mark.anyio
        async def test_returns_all_available_tags(
            self,
            available_tags: list[str],
            registered_user_client: AsyncClient,
        ) -> None:
            response = await registered_user_client.get("/tags")

            assert response.json() == {"tags": available_tags}
