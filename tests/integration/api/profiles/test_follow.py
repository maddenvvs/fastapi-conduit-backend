from typing import Any, AsyncGenerator, Callable

import pytest
from httpx import AsyncClient, Response

from conduit.infrastructure.persistence.models import UserModel
from tests.integration.conftest import AddToDb


class TestWhenFollowNonexistingProfile:
    @pytest.fixture
    async def profile_response(self, registered_user_client: AsyncClient) -> Response:
        return await registered_user_client.post(
            "/profiles/non-existing-username/follow",
        )

    @pytest.mark.anyio
    async def test_returns_404_not_found(self, profile_response: Response) -> None:
        assert profile_response.status_code == 404

    @pytest.mark.anyio
    async def test_returns_detailed_message(self, profile_response: Response) -> None:
        assert profile_response.json() == {"detail": "Profile not found"}


class TestWhenFollowYourself:
    @pytest.fixture
    async def follow_response(
        self,
        registered_user_client: AsyncClient,
        registered_user: UserModel,
    ) -> Response:
        return await registered_user_client.post(
            f"/profiles/{registered_user.username}/follow",
        )

    @pytest.mark.anyio
    async def test_returns_status_400(self, follow_response: Response) -> None:
        assert follow_response.status_code == 400

    @pytest.mark.anyio
    async def test_returns_detailed_message(self, follow_response: Response) -> None:
        assert follow_response.json() == {"detail": "Cannot follow yourself"}


class TestWhenFollowExistingProfile:
    @pytest.fixture(
        params=[
            "joe",
            "rachel",
            "chandler",
            "monica",
            "phoebe",
            "ross",
        ],
    )
    async def test_username(self, request: pytest.FixtureRequest) -> Any:
        return request.param

    @pytest.fixture
    async def test_user(
        self,
        test_username: str,
        user_model_factory: Callable[..., UserModel],
    ) -> UserModel:
        return user_model_factory(
            username=test_username,
            email="hero@friends.com",
        )

    @pytest.fixture(autouse=True)
    async def create_test_user(
        self,
        test_user: UserModel,
        add_to_db: AddToDb,
    ) -> None:
        await add_to_db(test_user)

    @pytest.fixture
    async def follow_response(
        self, registered_user_client: AsyncClient, test_username: str,
    ) -> AsyncGenerator[Response, None]:
        url = f"/profiles/{test_username}/follow"
        yield await registered_user_client.post(url)
        await registered_user_client.delete(url)

    @pytest.mark.anyio
    async def test_returns_202_status(self, follow_response: Response) -> None:
        assert follow_response.status_code == 202

    @pytest.mark.anyio
    async def test_has_followed_true(self, follow_response: Response) -> None:
        assert follow_response.json()["profile"]["following"] is True

    class TestAndItWasAlreadyFollowed:
        @pytest.fixture
        async def follow_response(
            self, registered_user_client: AsyncClient, test_username: str,
        ) -> AsyncGenerator[Response, None]:
            url = f"/profiles/{test_username}/follow"
            await registered_user_client.post(url)
            yield await registered_user_client.post(url)
            await registered_user_client.delete(url)

        @pytest.mark.anyio
        async def test_returns_status_400(self, follow_response: Response) -> None:
            assert follow_response.status_code == 400

        @pytest.mark.anyio
        async def test_returns_detailed_message(
            self, follow_response: Response,
        ) -> None:
            assert follow_response.json() == {"detail": "Profile is already followed"}
