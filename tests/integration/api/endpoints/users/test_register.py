from typing import Any, AsyncGenerator, Callable

import pytest
from httpx import AsyncClient, Response
from sqlalchemy import delete
from typing_extensions import TypeAlias

from conduit.infrastructure.persistence.database import Database
from conduit.infrastructure.persistence.models import UserModel

RegisterRequest: TypeAlias = dict[str, Any]
RequestFactory: TypeAlias = Callable[..., RegisterRequest]


@pytest.fixture
def register_request_factory() -> RequestFactory:
    def factory(**kwargs: Any) -> dict[str, Any]:
        default_values = dict(
            username="walkmansit",
            email="walkmansit@gmail.com",
            password="1qazxsw23edc",
        )
        return {
            "user": {
                **default_values,
                **kwargs,
            }
        }

    return factory


class TestWhenRegisteringWithInvalidRequestFields:

    @pytest.fixture(
        params=[
            {"username": ""},
            {"password": ""},
            {"email": ""},
            {"email": "@.cm"},
        ]
    )
    def invalid_register_request(
        self,
        request: pytest.FixtureRequest,
        register_request_factory: RequestFactory,
    ) -> RegisterRequest:
        return register_request_factory(**request.param)

    class TestForAnonymousUser:

        @pytest.fixture
        async def anonymous_response(
            self,
            anonymous_test_client: AsyncClient,
            invalid_register_request: RegisterRequest,
        ) -> Response:
            response = await anonymous_test_client.post(
                "/users", json=invalid_register_request
            )
            return response

        @pytest.mark.anyio
        async def test_returns_status_422(self, anonymous_response: Response) -> None:
            assert anonymous_response.status_code == 422

        @pytest.mark.anyio
        async def test_has_body_with_erros(self, anonymous_response: Response) -> None:
            r = anonymous_response.json()

            assert "errors" in r
            assert len(r["errors"]) > 0

    class TestForRegisteredUser:

        @pytest.fixture
        async def registered_user_response(
            self,
            registered_user_client: AsyncClient,
            invalid_register_request: RegisterRequest,
        ) -> Response:
            response = await registered_user_client.post(
                "/users", json=invalid_register_request
            )
            return response

        @pytest.mark.anyio
        async def test_returns_status_422(
            self, registered_user_response: Response
        ) -> None:
            assert registered_user_response.status_code == 422

        @pytest.mark.anyio
        async def test_has_body_with_erros(
            self, registered_user_response: Response
        ) -> None:
            r = registered_user_response.json()

            assert "errors" in r
            assert len(r["errors"]) > 0


class TestWhenRegisteredSuccessully:

    @pytest.fixture(
        params=[
            dict(username="ivan", password="clear", email="a@a.com"),
            dict(username="ivan", password="very_strong_one", email="a@aabc.com"),
            dict(username="gobyna", password="uncertain", email="booking@aabc.com"),
        ]
    )
    async def request_body(
        self,
        register_request_factory: RequestFactory,
        request: pytest.FixtureRequest,
    ) -> RegisterRequest:
        return register_request_factory(**request.param)

    @pytest.fixture
    async def successful_response(
        self,
        request_body: RegisterRequest,
        anonymous_test_client: AsyncClient,
        test_db: Database,
    ) -> AsyncGenerator[Response, None]:
        response = await anonymous_test_client.post(
            "/users",
            json=request_body,
        )

        yield response

        async with test_db.create_session() as session:
            await session.execute(
                delete(UserModel).where(
                    UserModel.email == request_body["user"]["email"]
                )
            )
            await session.commit()

    @pytest.mark.anyio
    async def test_returns_200_OK(self, successful_response: Response) -> None:
        assert successful_response.status_code == 201

    @pytest.mark.anyio
    async def test_returns_body_with_created_user_details(
        self,
        successful_response: Response,
        request_body: RegisterRequest,
    ) -> None:
        r = successful_response.json()

        assert len(r["user"]) == 5
        assert r["user"]["email"] == request_body["user"]["email"]
        assert r["user"]["username"] == request_body["user"]["username"]
        assert r["user"]["bio"] == ""
        assert r["user"]["image"] is None
        assert len(r["user"]["token"]) > 0


class TestWhenUsernameIsTaken:

    @pytest.fixture
    async def failed_response(
        self,
        registered_user: UserModel,
        anonymous_test_client: AsyncClient,
        register_request_factory: RequestFactory,
    ) -> Response:
        request = register_request_factory(username=registered_user.username)
        response = await anonymous_test_client.post("/users", json=request)
        return response

    @pytest.mark.anyio
    async def test_returns_422_status(self, failed_response: Response) -> None:
        assert failed_response.status_code == 422

    @pytest.mark.anyio
    async def test_returns_body_with_clarification(
        self, failed_response: Response
    ) -> None:
        assert failed_response.json() == {"errors": {"username": ["Username is taken"]}}


class TestWhenEmailIsTaken:

    @pytest.fixture
    async def failed_response(
        self,
        registered_user: UserModel,
        anonymous_test_client: AsyncClient,
        register_request_factory: RequestFactory,
    ) -> Response:
        request = register_request_factory(email=registered_user.email)
        response = await anonymous_test_client.post("/users", json=request)
        return response

    @pytest.mark.anyio
    async def test_returns_422_status(self, failed_response: Response) -> None:
        assert failed_response.status_code == 422

    @pytest.mark.anyio
    async def test_returns_body_with_clarification(
        self, failed_response: Response
    ) -> None:
        assert failed_response.json() == {"errors": {"email": ["Email is taken"]}}
