from typing import Any, AsyncGenerator, Callable

import pytest
from httpx import AsyncClient, Response

from conduit.infrastructure.persistence.database import Database
from conduit.infrastructure.persistence.models import UserModel


class TestWhenVisitingNonExistingProfile:

    @pytest.fixture
    async def profile_response(self, any_client: AsyncClient) -> Response:
        return await any_client.get("/profiles/non-existing-username")

    @pytest.mark.anyio
    async def test_returns_404_not_found(self, profile_response: Response) -> None:
        assert profile_response.status_code == 404

    @pytest.mark.anyio
    async def test_returns_detailed_message(self, profile_response: Response) -> None:
        assert profile_response.json() == {"detail": "Profile not found"}


class TestWhenVisitingExistingProfile:

    @pytest.fixture(
        params=[
            "joe",
            "rachel",
            "chandler",
            "monica",
            "phoebe",
            "ross",
        ]
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
        self, test_user: UserModel, test_db: Database
    ) -> AsyncGenerator[None, None]:
        async with test_db.create_session() as session:
            session.add(test_user)
            await session.commit()
            yield
            await session.delete(test_user)
            await session.commit()

    class TestForAnyClient:

        @pytest.fixture
        async def profile_response(
            self, any_client: AsyncClient, test_username: str
        ) -> Response:
            return await any_client.get(f"/profiles/{test_username}")

        @pytest.mark.anyio
        async def test_returns_200_OK(self, profile_response: Response) -> None:
            assert profile_response.status_code == 200

        @pytest.mark.anyio
        async def test_returns_profile_data(
            self,
            profile_response: Response,
            test_user: UserModel,
        ) -> None:
            assert profile_response.json() == {
                "profile": {
                    "username": test_user.username,
                    "bio": test_user.bio,
                    "image": test_user.image_url,
                    "following": False,
                },
            }

    class TestFollowedByCurrentUser:

        @pytest.fixture(autouse=True)
        async def follow_profile(
            self, test_username: str, registered_user_client: AsyncClient
        ) -> AsyncGenerator[None, None]:
            await registered_user_client.post(f"/profiles/{test_username}/follow")
            yield
            await registered_user_client.delete(f"/profiles/{test_username}/follow")

        @pytest.mark.anyio
        async def test_returns_following_true(
            self,
            registered_user_client: AsyncClient,
            test_username: str,
        ) -> None:
            response = await registered_user_client.get(f"/profiles/{test_username}")

            assert response.json()["profile"]["following"] is True
