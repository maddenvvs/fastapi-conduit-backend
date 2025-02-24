from datetime import datetime
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, Response

from conduit.infrastructure.persistence.database import Database
from conduit.infrastructure.persistence.models import UserModel


class TestWhenLoginWithEmptyPassword:

    @pytest.fixture
    async def empty_username_response(
        self, anonymous_test_client: AsyncClient
    ) -> Response:
        response = await anonymous_test_client.post(
            url="/users/login",
            json=dict(
                user=dict(
                    email="a@a.com",
                    password="",
                )
            ),
        )
        return response

    @pytest.mark.anyio
    async def test_returns_status_422_invalid_request(
        self, empty_username_response: Response
    ) -> None:
        assert empty_username_response.status_code == 422

    @pytest.mark.anyio
    async def test_returns_json_with_error_reason(
        self, empty_username_response: Response
    ) -> None:
        assert empty_username_response.json() == {
            "errors": {"password": ["String should have at least 1 character"]}
        }


class TestWhenLoginWithInvalidEmail:

    @pytest.fixture(
        params=[
            "",
            "abc",
            "a.com",
            "@.com",
            "b@.com",
            "@asdasd.com",
        ]
    )
    async def empty_password_response(
        self,
        request: pytest.FixtureRequest,
        anonymous_test_client: AsyncClient,
    ) -> Response:
        response = await anonymous_test_client.post(
            url="/users/login",
            json=dict(
                user=dict(
                    email=request.param,
                    password="password",
                )
            ),
        )
        return response

    @pytest.mark.anyio
    async def test_returns_status_422_invalid_request(
        self, empty_password_response: Response
    ) -> None:
        assert empty_password_response.status_code == 422

    @pytest.mark.anyio
    async def test_returns_json_with_error_reason(
        self, empty_password_response: Response
    ) -> None:
        json_response = empty_password_response.json()

        assert "errors" in json_response
        assert len(json_response["errors"]) == 1
        assert "email" in json_response["errors"]
        assert len(json_response["errors"]["email"]) > 0


class TestWhenLoginToNonExistingUser:
    @pytest.fixture(
        params=[
            dict(email="a@a.com", password="123"),
            dict(email="bob@company.io", password="password"),
            dict(email="alice@jets.co.uk", password="!paswd!d2ds"),
        ]
    )
    async def nonexisting_user_response(
        self,
        request: pytest.FixtureRequest,
        anonymous_test_client: AsyncClient,
    ) -> Response:
        param = request.param
        response = await anonymous_test_client.post(
            url="/users/login",
            json=dict(
                user=dict(
                    email=param["email"],
                    password=param["password"],
                )
            ),
        )
        return response

    @pytest.mark.anyio
    async def test_returns_status_401_unauthorized(
        self, nonexisting_user_response: Response
    ) -> None:
        assert nonexisting_user_response.status_code == 401

    @pytest.mark.anyio
    async def test_returns_empty_response(
        self, nonexisting_user_response: Response
    ) -> None:
        assert nonexisting_user_response.json() is None


class TestWhenLoginToExistingUser:

    @pytest.fixture(autouse=True)
    async def create_valid_user(self, test_db: Database) -> AsyncGenerator[None, None]:
        async with test_db.create_session() as session:
            user = UserModel(
                username="walkmansit",
                email="walkmansit@gmail.com",
                password_hash="very_strong_password",
                bio="Some bio about me.",
                image_url=None,
                created_at=datetime(year=2020, month=1, day=1),
                updated_at=datetime(year=2020, month=1, day=1),
            )
            session.add(user)
            await session.commit()
            yield
            await session.delete(user)
            await session.commit()

    class TestWithValidCredentials:

        @pytest.fixture
        async def valid_login_response(
            self, anonymous_test_client: AsyncClient
        ) -> Response:
            response = await anonymous_test_client.post(
                url="/users/login",
                json=dict(
                    user=dict(
                        email="walkmansit@gmail.com",
                        password="very_strong_password",
                    )
                ),
            )
            return response

        @pytest.mark.anyio
        async def test_returns_status_200_OK(
            self, valid_login_response: Response
        ) -> None:
            assert valid_login_response.status_code == 200

        @pytest.mark.anyio
        async def test_returns_jwt_token(self, valid_login_response: Response) -> None:
            json_response = valid_login_response.json()

            assert len(json_response["user"]["token"]) > 0

    class TestWithInvalidPassword:

        @pytest.fixture
        async def invalid_login_response(
            self, anonymous_test_client: AsyncClient
        ) -> Response:
            response = await anonymous_test_client.post(
                url="/users/login",
                json=dict(
                    user=dict(
                        email="walkmansit@gmail.com",
                        password="invalid_password",
                    )
                ),
            )
            return response

        @pytest.mark.anyio
        async def test_returns_status_401_unauthorized(
            self, invalid_login_response: Response
        ) -> None:
            assert invalid_login_response.status_code == 401

        @pytest.mark.anyio
        async def test_returns_empty_body(
            self, invalid_login_response: Response
        ) -> None:
            assert invalid_login_response.json() is None
