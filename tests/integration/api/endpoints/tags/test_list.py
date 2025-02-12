import pytest
from fastapi import status
from httpx import AsyncClient


class TestSuccessfullyListTags:

    @pytest.mark.anyio
    async def test_returns_status_OK_for_anonymous_user(
        self,
        anonymous_test_client: AsyncClient,
    ):
        response = await anonymous_test_client.get("/tags")

        assert response.status_code == status.HTTP_200_OK
