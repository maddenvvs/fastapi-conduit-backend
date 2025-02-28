from typing import Any

import pytest
from httpx import AsyncClient, Response


class TestWhenUpdateWithInvalidFields:
    @pytest.fixture(
        params=[
            dict(email=""),
            dict(password=""),
            dict(username=""),
            dict(image=""),
            dict(image="qwdw"),
            dict(image="ftp://asdt:2301/images/cat.jpeg"),
        ]
    )
    def invalid_fields(self, request: pytest.FixtureRequest) -> Any:
        return request.param

    @pytest.fixture
    async def update_response(
        self, invalid_fields: dict[str, Any], registered_user_client: AsyncClient
    ) -> Response:
        return await registered_user_client.put("/user", json={"user": invalid_fields})

    @pytest.mark.anyio
    async def test_returns_422_status(self, update_response: Response) -> None:
        assert update_response.status_code == 422

    @pytest.mark.anyio
    async def test_returns_errors_body(self, update_response: Response) -> None:
        assert len(update_response.json()["errors"]) == 1
