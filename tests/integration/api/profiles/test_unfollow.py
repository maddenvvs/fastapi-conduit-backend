from typing import Any

import pytest
from httpx import AsyncClient, Response

from conduit.infrastructure.persistence.models import UserModel
from tests.integration.conftest import AddToDb, UserModelFactory


class TestWhenUnfollowNonexistingProfile:
    @pytest.fixture
    async def unfollow_response(self, registered_user_client: AsyncClient) -> Response:
        return await registered_user_client.delete(
            "/profiles/non-existing-username/follow",
        )

    @pytest.mark.anyio
    async def test_returns_404_not_found(self, unfollow_response: Response) -> None:
        assert unfollow_response.status_code == 404

    @pytest.mark.anyio
    async def test_returns_detailed_message(self, unfollow_response: Response) -> None:
        assert unfollow_response.json() == {"detail": "Profile not found"}


class TestWhenUnfollowYourself:
    @pytest.fixture
    async def unfollow_response(
        self,
        registered_user_client: AsyncClient,
        registered_user: UserModel,
    ) -> Response:
        return await registered_user_client.delete(
            f"/profiles/{registered_user.username}/follow",
        )

    @pytest.mark.anyio
    async def test_returns_status_400(self, unfollow_response: Response) -> None:
        assert unfollow_response.status_code == 400

    @pytest.mark.anyio
    async def test_returns_detailed_message(self, unfollow_response: Response) -> None:
        assert unfollow_response.json() == {"detail": "Cannot unfollow yourself"}


class TestWhenUnfollowExistingProfile:
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
        user_model_factory: UserModelFactory,
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
    async def unfollow_response(
        self,
        registered_user_client: AsyncClient,
        test_username: str,
    ) -> Response:
        url = f"/profiles/{test_username}/follow"
        return await registered_user_client.delete(url)

    @pytest.mark.anyio
    async def test_returns_400_status(self, unfollow_response: Response) -> None:
        assert unfollow_response.status_code == 400

    @pytest.mark.anyio
    async def test_has_followed_true(self, unfollow_response: Response) -> None:
        assert unfollow_response.json() == {"detail": "Profile is already unfollowed"}

    class TestAndItWasAlreadyFollowed:
        @pytest.fixture
        async def unfollow_response(
            self, registered_user_client: AsyncClient, test_username: str,
        ) -> Response:
            url = f"/profiles/{test_username}/follow"
            await registered_user_client.post(url)
            return await registered_user_client.delete(url)

        @pytest.mark.anyio
        async def test_returns_status_202(self, unfollow_response: Response) -> None:
            assert unfollow_response.status_code == 202

        @pytest.mark.anyio
        async def test_returns_following_false(
            self, unfollow_response: Response,
        ) -> None:
            assert unfollow_response.json()["profile"]["following"] is False
