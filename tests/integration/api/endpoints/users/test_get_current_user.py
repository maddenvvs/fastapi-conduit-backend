import pytest
from httpx import AsyncClient, Response

from conduit.infrastructure.persistence.models import UserModel


class TestWhenVisitingAnonymously:

    @pytest.fixture
    async def anonymous_response(self, anonymous_test_client: AsyncClient) -> Response:
        response = await anonymous_test_client.get("/user")
        return response

    @pytest.mark.anyio
    async def test_returns_status_401_unauthorized(
        self, anonymous_response: Response
    ) -> None:
        assert anonymous_response.status_code == 401

    @pytest.mark.anyio
    async def test_returns_empty_body(self, anonymous_response: Response) -> None:
        assert anonymous_response.json() == {
            "detail": "Missing authorization credentials."
        }


class TestWhenVisitingByRegisteredUser:

    @pytest.fixture
    async def registered_user_response(
        self, registered_user_client: AsyncClient
    ) -> Response:
        response = await registered_user_client.get("/user")
        return response

    @pytest.mark.anyio
    async def test_returns_status_200_OK(
        self, registered_user_response: Response
    ) -> None:
        assert registered_user_response.status_code == 200

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
