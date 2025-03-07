import pytest
from httpx import AsyncClient, Response, codes

from conduit.infrastructure.common.persistence.models import UserModel


class TestWhenVisitingByRegisteredUser:
    @pytest.fixture
    async def registered_user_response(
        self,
        registered_user_client: AsyncClient,
    ) -> Response:
        return await registered_user_client.get("/user")

    @pytest.mark.anyio
    async def test_returns_status_ok(
        self,
        registered_user_response: Response,
    ) -> None:
        assert registered_user_response.status_code == codes.OK

    @pytest.mark.anyio
    async def test_returns_user_details_with_token(
        self,
        registered_user_response: Response,
        registered_user: UserModel,
        registered_user_token: str,
    ) -> None:
        assert registered_user_response.json() == {
            "user": {
                "email": registered_user.email,
                "username": registered_user.username,
                "bio": registered_user.bio,
                "image": registered_user.image_url,
                "token": registered_user_token,
            },
        }
